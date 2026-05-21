#!/usr/bin/env python3
"""03_cloud_attr.py — attribute each resolved IP to a cloud provider.

Strategy:
  1. Download published IPv4 CIDR ranges from AWS, GCP, Oracle, Cloudflare.
  2. For each IP in resolved.csv, find the first matching prefix.
  3. If no public range matched, fall back to Team Cymru's `whois -h whois.cymru.com`
     bulk lookup to get the ASN holder (covers Azure, UCI on-prem, third-party SaaS).

Usage: scripts/03_cloud_attr.py data/resolved.csv
Output: data/cloud_hosts.csv with columns: subdomain,ip,provider,detail
"""
import csv
import ipaddress
import json
import socket
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

RANGE_SOURCES = {
    "AWS":        "https://ip-ranges.amazonaws.com/ip-ranges.json",
    "GCP":        "https://www.gstatic.com/ipranges/cloud.json",
    "Oracle":     "https://docs.oracle.com/iaas/tools/public_ip_ranges.json",
    "Cloudflare": "https://www.cloudflare.com/ips-v4",
}

# Hard-coded fast paths. Saves a Cymru lookup for ~half the resolved IPs
# (UCI is its own AS, so any campus / health-system IP would otherwise
# fall to the ASN fallback). RFC1918 IPs that leak into public DNS are a
# finding in themselves and get their own bucket.
UCI_PREFIXES = [
    ("128.195.0.0/16", "UCI campus (UCI-NET, AS3127)"),
    ("128.200.0.0/16", "UCI campus (UCI-NET, AS3127)"),
    ("169.234.0.0/16", "UCI campus (UCI-NET, AS3127)"),
    ("160.87.0.0/16",  "UCI Health (UCIMC-NET)"),
]
RFC1918_PREFIXES = [
    ("10.0.0.0/8",     "RFC1918 — internal IP leaked to public DNS"),
    ("172.16.0.0/12",  "RFC1918 — internal IP leaked to public DNS"),
    ("192.168.0.0/16", "RFC1918 — internal IP leaked to public DNS"),
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "swe267p-recon"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode()


def load_ranges():
    """Return list[(network, provider, detail)]."""
    out = []
    # Local fast-paths first so they win over any overlapping cloud range.
    for cidr, detail in UCI_PREFIXES:
        out.append((ipaddress.ip_network(cidr), "UCI on-prem", detail))
    for cidr, detail in RFC1918_PREFIXES:
        out.append((ipaddress.ip_network(cidr), "RFC1918 (leaked)", detail))
    print("[*] fetching CSP IP ranges...", file=sys.stderr)
    aws = json.loads(fetch(RANGE_SOURCES["AWS"]))
    for p in aws["prefixes"]:
        out.append((ipaddress.ip_network(p["ip_prefix"]), "AWS", p.get("service", "") + "/" + p.get("region", "")))
    gcp = json.loads(fetch(RANGE_SOURCES["GCP"]))
    for p in gcp["prefixes"]:
        if "ipv4Prefix" in p:
            out.append((ipaddress.ip_network(p["ipv4Prefix"]), "GCP", p.get("service", "") + "/" + p.get("scope", "")))
    oci = json.loads(fetch(RANGE_SOURCES["Oracle"]))
    for region in oci["regions"]:
        for p in region["cidrs"]:
            out.append((ipaddress.ip_network(p["cidr"]), "Oracle", region["region"]))
    cf = fetch(RANGE_SOURCES["Cloudflare"]).splitlines()
    for line in cf:
        line = line.strip()
        if line:
            out.append((ipaddress.ip_network(line), "Cloudflare", "edge"))
    print(f"[+] loaded {len(out)} CIDR ranges", file=sys.stderr)
    return out


def match_cidr(ip, ranges):
    ip_obj = ipaddress.ip_address(ip)
    for net, provider, detail in ranges:
        if ip_obj in net:
            return provider, detail
    return None


def cymru_bulk(ips):
    """Bulk ASN lookup via Team Cymru's netcat-style whois server.
       Returns {ip: 'ASN | holder'}.
    """
    if not ips:
        return {}
    out = {}
    try:
        s = socket.create_connection(("whois.cymru.com", 43), timeout=20)
        payload = "begin\nverbose\n" + "\n".join(sorted(ips)) + "\nend\n"
        s.sendall(payload.encode())
        buf = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            buf += chunk
        s.close()
        for line in buf.decode(errors="ignore").splitlines():
            if line.startswith("Bulk") or not line.strip():
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 7:
                asn, ip, _, _, _, _, holder = parts[:7]
                out[ip] = f"AS{asn} {holder}"
    except OSError as e:
        print(f"[!] cymru lookup failed: {e}", file=sys.stderr)
    return out


def classify_holder(holder):
    h = holder.lower()
    if "amazon" in h or "aws" in h:               return "AWS"
    if "google" in h:                              return "GCP"
    if "microsoft" in h or "azure" in h:           return "Azure"
    if "cloudflare" in h:                          return "Cloudflare"
    if "oracle" in h:                              return "Oracle"
    if "fastly" in h:                              return "Fastly"
    if "akamai" in h:                              return "Akamai"
    if "digitalocean" in h:                        return "DigitalOcean"
    if "linode" in h:                              return "Linode"
    if "salesforce" in h:                          return "Salesforce"
    if "github" in h:                              return "GitHub"
    if "shopify" in h:                             return "Shopify"
    if "wpengine" in h or "wp engine" in h:        return "WPEngine"
    if "pantheon" in h:                            return "Pantheon"
    if "incapsula" in h or "imperva" in h:         return "Imperva"
    if "ucnet" in h or "university of california" in h or "irvine" in h:
        return "UCI on-prem / UCnet"
    return "Other"


def main():
    in_path = Path(sys.argv[1] if len(sys.argv) > 1 else "data/resolved.csv")
    out_path = in_path.with_name("cloud_hosts.csv")

    rows = list(csv.DictReader(in_path.open()))
    unique_ips = sorted({r["ip"] for r in rows})
    print(f"[*] {len(rows)} rows, {len(unique_ips)} unique IPs", file=sys.stderr)

    ranges = load_ranges()
    cached = {}
    for ip in unique_ips:
        m = match_cidr(ip, ranges)
        if m:
            cached[ip] = (m[0], m[1])

    missing = [ip for ip in unique_ips if ip not in cached]
    print(f"[*] CIDR-match: {len(cached)}, falling back to ASN for {len(missing)}", file=sys.stderr)
    asn_map = cymru_bulk(missing)
    for ip in missing:
        holder = asn_map.get(ip, "unknown")
        cached[ip] = (classify_holder(holder), holder)

    with out_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["subdomain", "ip", "provider", "detail"])
        for r in rows:
            provider, detail = cached[r["ip"]]
            w.writerow([r["subdomain"], r["ip"], provider, detail])

    # quick summary
    counts = defaultdict(int)
    for r in rows:
        counts[cached[r["ip"]][0]] += 1
    print("[+] per-provider subdomain counts:", file=sys.stderr)
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"    {k:30s} {v}", file=sys.stderr)
    print(f"[+] wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

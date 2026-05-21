#!/usr/bin/env bash
# 02_resolve.sh — resolve subdomains to IPv4 A records in parallel.
# Output: data/resolved.csv with columns: subdomain,ip
# Subdomains with no A record are skipped (they are CNAME-only dangling or NXDOMAIN).
#
# Usage: scripts/02_resolve.sh data/subdomains.txt
set -euo pipefail

IN="${1:-data/subdomains.txt}"
OUT_DIR="$(cd "$(dirname "$0")/.." && pwd)/data"
OUT="$OUT_DIR/resolved.csv"

echo "subdomain,ip" > "$OUT"

resolve_one() {
  local sub="$1"
  # +short A returns one IP per line; suppress CNAME chains by filtering for dotted-quad.
  # @1.1.1.1 uses Cloudflare resolver (consistent, fast) — avoids local resolver caching surprises.
  dig @1.1.1.1 +short +time=2 +tries=1 A "$sub" 2>/dev/null \
    | grep -E '^([0-9]{1,3}\.){3}[0-9]{1,3}$' \
    | while read -r ip; do echo "$sub,$ip"; done
}
export -f resolve_one

echo "[*] resolving $(wc -l < "$IN") subdomains (parallel)..."
# xargs -P 200 — bulk resolution against 1.1.1.1, which handles this load fine.
< "$IN" xargs -I{} -P 200 bash -c 'resolve_one "$@"' _ {} >> "$OUT"

echo "[+] resolved pairs: $(($(wc -l < "$OUT") - 1)) -> $OUT"
echo "[+] unique IPs:     $(tail -n +2 "$OUT" | cut -d, -f2 | sort -u | wc -l)"

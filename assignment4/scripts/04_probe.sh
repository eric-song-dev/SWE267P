#!/usr/bin/env bash
# 04_probe.sh — HTTP/HTTPS probe each resolved subdomain.
# Output: data/probe.csv with columns: url,status,server,title
# Probes https first, falls back to http if https fails.
#
# Usage: scripts/04_probe.sh data/resolved.csv
set -euo pipefail

IN="${1:-data/resolved.csv}"
OUT_DIR="$(cd "$(dirname "$0")/.." && pwd)/data"
OUT="$OUT_DIR/probe.csv"

echo "url,status,server,title" > "$OUT"

probe_one() {
  local sub="$1"
  for scheme in https http; do
    local url="$scheme://$sub"
    local resp
    resp=$(curl -sk --max-time 8 -o /tmp/probe_body.$$ -w '%{http_code}|%{header_json}' "$url" 2>/dev/null) || continue
    local status="${resp%%|*}"
    local headers="${resp#*|}"
    [[ "$status" == "000" ]] && continue
    local server
    server=$(printf '%s' "$headers" | jq -r '.server[0] // ""' 2>/dev/null | tr ',' ' ' | head -c 80)
    local title
    title=$(grep -oiE '<title[^>]*>[^<]*</title>' /tmp/probe_body.$$ 2>/dev/null \
            | head -1 | sed -e 's/<[^>]*>//g' -e 's/[[:space:]]\+/ /g' -e 's/^ //' -e 's/ $//' \
            | tr ',' ' ' | head -c 120)
    echo "$url,$status,$server,$title"
    rm -f /tmp/probe_body.$$
    return
  done
  rm -f /tmp/probe_body.$$
}
export -f probe_one

# unique subdomains
tail -n +2 "$IN" | cut -d, -f1 | sort -u > /tmp/probe_subs.$$
echo "[*] probing $(wc -l < /tmp/probe_subs.$$) unique subdomains..."

< /tmp/probe_subs.$$ xargs -I{} -P 30 bash -c 'probe_one "$@"' _ {} >> "$OUT"
rm -f /tmp/probe_subs.$$

echo "[+] probe results: $(($(wc -l < "$OUT") - 1)) -> $OUT"

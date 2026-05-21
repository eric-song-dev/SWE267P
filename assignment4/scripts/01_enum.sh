#!/usr/bin/env bash
# 01_enum.sh — passive subdomain enumeration for a target domain.
# Sources: subfinder (aggregates many passive APIs) + crt.sh (CT logs).
# Output: data/subdomains.txt (one subdomain per line, deduped, sorted).
#
# Usage: scripts/01_enum.sh uci.edu
set -euo pipefail

DOMAIN="${1:-uci.edu}"
OUT_DIR="$(cd "$(dirname "$0")/.." && pwd)/data"
mkdir -p "$OUT_DIR"

echo "[*] subfinder -d $DOMAIN"
subfinder -d "$DOMAIN" -silent -all > "$OUT_DIR/subdomains_subfinder.txt"

echo "[*] crt.sh certificate-transparency query"
curl -s "https://crt.sh/?q=%25.${DOMAIN}&output=json" \
  | jq -r '.[].name_value' \
  | tr '[:upper:]' '[:lower:]' \
  | sed 's/^\*\.//' \
  | tr '\n' '\n' \
  | grep -E "\.${DOMAIN//./\\.}$" \
  | sort -u > "$OUT_DIR/subdomains_crtsh.txt"

cat "$OUT_DIR/subdomains_subfinder.txt" "$OUT_DIR/subdomains_crtsh.txt" \
  | sort -u > "$OUT_DIR/subdomains.txt"

echo "[+] subfinder: $(wc -l < "$OUT_DIR/subdomains_subfinder.txt")"
echo "[+] crt.sh:    $(wc -l < "$OUT_DIR/subdomains_crtsh.txt")"
echo "[+] merged:    $(wc -l < "$OUT_DIR/subdomains.txt") -> $OUT_DIR/subdomains.txt"

#!/usr/bin/env bash

data=$(curl -fsS http://127.0.0.1:8000/packages.json)

{
  echo "# Summary for Active Packages"
  echo ""
  echo "| name | version | downloads |"
  echo "|------|---------|-----------|"
  echo "$data" | jq -r '.[] | select(.status == "active" and .downloads >= 100) | [.name, .version, .downloads] | @tsv' \
    | sort -k3,3nr -k1,1 \
    | awk -F'\t' '{printf "| %s | %s | %s |\n", $1, $2, $3}'
} > summary.md

echo "Report written to summary.md"

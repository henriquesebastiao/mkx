#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <target>"
  exit 1
fi

TARGET=$1
DATE=$(date +'%Y-%m-%d_%H-%M-%S')
OUTPUT_FILE="nmap_output_${DATE}.txt"

sudo nmap -sU -p 161 --open -oG "$OUTPUT_FILE" "$TARGET"

echo "Scan completed! Results saved to: $OUTPUT_FILE"

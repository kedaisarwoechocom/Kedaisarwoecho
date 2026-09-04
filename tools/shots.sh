#!/bin/sh
# Captures aux largeurs de reference.  usage: sh tools/shots.sh [suffixe]
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
SUF="$1"
URL="${2:-http://127.0.0.1:8899/index.html}"
mkdir -p build/shots
shoot() {
  W="$1"; H="$2"
  DEST=$(printf 'E:\c\projet\Kedaisarwoecho\build\shots\%s%s.png' "$W" "$SUF")
  "$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
    --user-data-dir="C:/Users/saido/AppData/Local/Temp/claude/chr-kse-$W" \
    --force-device-scale-factor=1 --virtual-time-budget=6000 \
    --window-size="$W,$H" --screenshot="$DEST" "$URL" >/dev/null 2>&1
  printf '  %-5s -> %s\n' "$W" "$(basename "$DEST")"
}
shoot 360 1500
shoot 390 1500
shoot 768 1600
shoot 1024 1250
shoot 1440 1024

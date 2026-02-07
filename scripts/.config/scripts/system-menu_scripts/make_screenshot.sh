#!/usr/bin/env bash

# ----------------------------------------------------- #
# Setup & Variables                                     #
# ----------------------------------------------------- #
SAVE_DIR="$HOME/Pictures/Screenshots"
mkdir -p "$SAVE_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Get active monitor name
MONITOR=$(hyprctl monitors -j | jq -r '.[] | select(.focused == true) | .name')

# ----------------------------------------------------- #
# Capture Logic                                         #
# ----------------------------------------------------- #
case "$1" in
    --full)
        filename="$SAVE_DIR/full_$TIMESTAMP.png"
        # Delay and capture only active monitor
        sleep 0.2 && grim -o "$MONITOR" "$filename"
        msg="Full screen ($MONITOR) captured"
        ;;
    --area)
        filename="$SAVE_DIR/area_$TIMESTAMP.png"
        grim -g "$(slurp)" "$filename"
        msg="Area captured"
        ;;
    --window)
        filename="$SAVE_DIR/window_$TIMESTAMP.png"
        # Delay and capture active window
        sleep 0.2 && grim -g "$(hyprctl activewindow -j | jq -r '"\(.at[0]),\(.at[1]) \(.size[0])x\(.size[1])"')" "$filename"
        msg="Window captured"
        ;;
    *)
        echo "Usage: $0 {--full|--area|--window}"
        exit 1
        ;;
esac

# ----------------------------------------------------- #
# Action & Notification                                 #
# ----------------------------------------------------- #
if [ -f "$filename" ]; then
    wl-copy < "$filename"
    notify-send -i camera-photo "Screenshot" "$msg\nSaved and copied to clipboard"
fi

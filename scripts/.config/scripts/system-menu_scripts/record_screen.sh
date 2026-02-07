#!/usr/bin/env bash

# -----------------------------------------------------
# Setup & Variables
# -----------------------------------------------------
SAVE_DIR="$HOME/Videos/Screenrecords"
mkdir -p "$SAVE_DIR"

# -----------------------------------------------------
# Recording Logic
# -----------------------------------------------------
if pgrep -x "wf-recorder" > /dev/null; then
    # Stop Recording
    pkill -INT wf-recorder
    notify-send -i camera-video "Recording stopped" "Video saved to $SAVE_DIR"
    exit 0
else
    # Start Recording
    filename="$SAVE_DIR/rec_$(date +%Y%m%d_%H%M%S).mp4"
    AUDIO_DEVICE=$(pactl get-default-sink).monitor
    
    notify-send -i camera-video "Recording started"
    sleep 0.2
    
    wf-recorder --audio="$AUDIO_DEVICE" -c libx264 -p preset=ultrafast -f "$filename" &
fi

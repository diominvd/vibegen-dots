#!/usr/bin/env bash

# Настройки
TEMP="5000"
ICON_ON=""
ICON_OFF=""

get_brightness() {
    local current max
    current=$(brightnessctl get 2>/dev/null)
    max=$(brightnessctl max 2>/dev/null)
    if [ -z "$max" ] || [ "$max" -le 0 ]; then
        echo "0"
    else
        awk -v cur="$current" -v mx="$max" 'BEGIN { printf "%.0f", (cur / mx) * 100 }'
    fi
}

if [[ "$1" == "--toggle" ]]; then
    if pgrep -x "hyprsunset" > /dev/null; then
        pkill -x "hyprsunset"
    else
        hyprsunset --temperature "$TEMP" > /dev/null 2>&1 &
    fi
    sleep 0.1
fi

BRIGHTNESS=$(get_brightness)

if pgrep -x "hyprsunset" > /dev/null; then
    echo "{\"text\":\"$ICON_ON  $BRIGHTNESS%\", \"class\":\"on\"}"
else
    echo "{\"text\":\"$ICON_OFF  $BRIGHTNESS%\", \"class\":\"off\"}"
fi

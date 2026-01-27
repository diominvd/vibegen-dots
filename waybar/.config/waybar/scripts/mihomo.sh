#!/bin/bash

BIN_PATH="/usr/bin/mihomo"
CONFIG_DIR="/home/diominvd/.config/mihomo"
PORT=9093

is_active() {
    if pgrep -x "mihomo" > /dev/null; then
        return 0
    else
        return 1
    fi
}

cleanup() {
    sudo pkill -9 -x "mihomo" > /dev/null 2>&1
    sudo fuser -k $PORT/tcp > /dev/null 2>&1
    sudo ip link delete tun0 > /dev/null 2>&1
}

if [ "$1" == "--toggle" ]; then
    if is_active; then
        cleanup
    else
        cleanup
        sleep 0.2
        sudo $BIN_PATH -d "$CONFIG_DIR" > /dev/null 2>&1 &
        disown
    fi
    exit 0
fi

if is_active; then
    echo "{\"text\": \"󰖟 ON\", \"class\": \"connected\", \"tooltip\": \"VPN Active\"}"
else
    echo "{\"text\": \"󰖟 OFF\", \"class\": \"disconnected\", \"tooltip\": \"VPN Offline\"}"
fi

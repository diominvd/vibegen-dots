#!/bin/bash

case "$1" in
    "hide")
        hyprctl dispatch movetoworkspacesilent special:minimized
        ;;
    "show")
        hyprctl dispatch togglespecialworkspace minimized
        ;;
    *)
        COUNT=$(hyprctl clients -j | jq '[.[] | select(.workspace.name == "special:minimized")] | length')
        
        if [ "$COUNT" -gt 0 ]; then
            echo "{\"text\":\"<span foreground='#d4be98'> </span>\",\"class\":\"minimized\"}"
        else
            echo "{\"text\":\"\",\"class\":\"empty\"}"
        fi
        ;;
esac

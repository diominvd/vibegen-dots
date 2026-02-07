#!/bin/bash

# -----------------------------------------------------
# Help & Arguments
# -----------------------------------------------------
show_help() {
    echo "Usage: $(basename "$0") [-t (time)] [-s (size)]"
    exit 0
}

SORT_BY="time"
while getopts "tsh" opt; do
    case "$opt" in
        t) SORT_BY="time" ;;
        s) SORT_BY="size" ;;
        *) show_help ;;
    esac
done

# -----------------------------------------------------
# Dependencies & Checks
# -----------------------------------------------------
for cmd in expac numfmt column; do
    command -v "$cmd" &>/dev/null || { echo "Error: $cmd missing."; exit 1; }
done

mapfile -t PKGS < <(pacman -Qeq)
[[ ${#PKGS[@]} -eq 0 ]] && { echo "No packages found."; exit 0; }

# -----------------------------------------------------
# Data Processing
# -----------------------------------------------------
DATA=$(expac --timefmt='%Y-%m-%d %H:%M:%S' '%l\t%m\t%n' -Q "${PKGS[@]}")

if [ "$SORT_BY" == "time" ]; then
    SORTED=$(echo "$DATA" | sort)
else
    SORTED=$(echo "$DATA" | sort -k2 -n)
fi

# -----------------------------------------------------
# Output
# -----------------------------------------------------
{
    echo -e "DATE\tTIME\tSIZE\tPACKAGE"
    echo "$SORTED" | while read -r d t s n; do
        echo -e "$d\t$t\t$(numfmt --to=iec-i --suffix=B "$s")\t$n"
    done
} | column -t -s $'\t'

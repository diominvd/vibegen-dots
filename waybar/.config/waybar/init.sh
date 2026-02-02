#!/bin/bash

# Path definitions
WAYBAR_DIR="$HOME/.config/waybar"
COMPONENTS_DIR="$WAYBAR_DIR/components"
THEMES_DIR="$WAYBAR_DIR/themes"

# Color definitions for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Waybar Symlink Initializer ===${NC}"

# 1. Ensure components directory exists
if [ ! -d "$COMPONENTS_DIR" ]; then
    mkdir -p "$COMPONENTS_DIR"
    echo -e "${GREEN}Created components directory.${NC}"
fi

# 2. Helper function to create symlinks
# Args: source_path_relative_to_themes target_name_in_components
make_link() {
    local source="$THEMES_DIR/$1"
    local target="$COMPONENTS_DIR/$2"

    if [ -f "$source" ]; then
        ln -sf "$source" "$target"
        echo -e "${GREEN}Linked:${NC} $2 -> $1"
    else
        echo -e "${RED}Error:${NC} Source not found: $1"
    fi
}

# 3. Initialize base components (Defaults)
echo -e "\n${BLUE}Initializing base components...${NC}"

# Monitor configuration (Critical for Rofi menu to detect the category)
make_link "panel/monitors/stock.jsonc" "panel-monitors.jsonc"

# Visual styles and positioning
make_link "panel/colors/filled.css" "panel-color.css"
make_link "panel/positions/sticky.jsonc" "panel-position.jsonc"

# Default Preset (Monochrome)
make_link "panel/presets/monochrome/monochrome.jsonc" "panel-preset.jsonc"
make_link "panel/presets/monochrome/monochrome.css" "widgets-style.css"

# 4. Initialize scripts folder from preset
echo -e "\n${BLUE}Initializing scripts folder...${NC}"
SCRIPTS_TARGET="$WAYBAR_DIR/scripts"
SCRIPTS_SOURCE="$THEMES_DIR/panel/presets/monochrome/scripts"

if [ -d "$SCRIPTS_SOURCE" ]; then
    # If scripts is a real directory (not a symlink), move to backup
    if [ -d "$SCRIPTS_TARGET" ] && [ ! -L "$SCRIPTS_TARGET" ]; then
        mv "$SCRIPTS_TARGET" "${SCRIPTS_TARGET}.backup"
        echo -e "${YELLOW}Existing scripts folder moved to scripts.backup${NC}"
    fi
    ln -sf "$SCRIPTS_SOURCE" "$SCRIPTS_TARGET"
    echo -e "${GREEN}Linked scripts

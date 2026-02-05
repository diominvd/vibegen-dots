import os
import re
import subprocess
import framework
from dataclasses import dataclass, field
from typing import List

HOME = os.path.expanduser("~")
SCRIPTS_DIR = f"{HOME}/.config/scripts/system-menu_scripts"

@dataclass(frozen=True)
class RofiStyle:
    # Element dimensions (all in pixels)
    ELEMENT_TEXT_HEIGHT: int = 20
    ELEMENT_PADDING_VERTICAL: int = 4
    ELEMENT_PADDING_HORIZONTAL: int = 12
    ELEMENT_BORDER_RADIUS: int = 12
    
    # Inputbar dimensions
    INPUTBAR_TEXT_HEIGHT: int = 20
    INPUTBAR_PADDING_VERTICAL: int = 8
    INPUTBAR_PADDING_HORIZONTAL: int = 12
    INPUTBAR_MARGIN_BOTTOM: int = 12
    
    # Listview and window dimensions
    LISTVIEW_SPACING: int = 4
    WINDOW_PADDING: int = 15
    WINDOW_BORDER_WIDTH: int = 4
    
    # Width and lines configuration for different menus
    DEFAULT_WIDTH: int = 300
    DEFAULT_LINES: int = 7
    WIDTH_CONFIG: dict = field(default_factory=lambda: {"Radio": 350})
    LINES_CONFIG: dict = field(default_factory=lambda: {"Apps": 6})

    # Colors and icons
    ACCENT_COLOR: str = "@accent"
    SECONDARY_TEXT_COLOR: str = "#6272a4"
    ICON_SIZE_DEFAULT: int = 20
    ICON_SIZE_PREVIEW: int = 20

    def get_width(self, node_name: str) -> int:
        return self.WIDTH_CONFIG.get(node_name, self.DEFAULT_WIDTH)

    def get_lines_limit(self, node_name: str) -> int:
        return self.LINES_CONFIG.get(node_name, self.DEFAULT_LINES)

STYLE = RofiStyle()

def clean_selection_name(selection: str) -> str:
    res = selection.split("\0icon")[0]
    if "\t" in res:
        res = res.split("\t")[0]
    res = re.sub(r'<[^>]+>', '', res)
    if ":" in res:
        res = res.split(":")[0]
    res = res.strip()
    if "  " in res:
        parts = res.split("  ", 1)
        if len(parts) > 1:
            res = parts[1]
    return res.strip()

def build_rofi_theme(lines: int, has_search: bool, width: int, show_icons: bool) -> str:
    """Generates Rofi theme with exact dimensions from STYLE."""
    s = STYLE
    
    icon_size = s.ICON_SIZE_PREVIEW if show_icons else s.ICON_SIZE_DEFAULT
    icon_css = f"enabled: true; size: {icon_size}px; margin: 0 12px 0 0;" if show_icons else "enabled: false;"
    
    return f"""
        configuration {{ show-icons: {'true' if show_icons else 'false'}; }}
        
        window {{ 
            width: {width}px; 
            border: {s.WINDOW_BORDER_WIDTH}px; 
        }}
        
        mainbox {{ 
            padding: {s.WINDOW_PADDING}px; 
            spacing: 0px; 
            children: [ {'"inputbar", ' if has_search else ''}"listview" ]; 
        }}
        
        inputbar {{ 
            enabled: {'true' if has_search else 'false'}; 
            padding: {s.INPUTBAR_PADDING_VERTICAL}px {s.INPUTBAR_PADDING_HORIZONTAL}px; 
            margin: 0 0 {s.INPUTBAR_MARGIN_BOTTOM}px 0; 
        }}
        
        listview {{ 
            lines: {lines}; 
            fixed-height: true; 
            dynamic: false; 
            spacing: {s.LISTVIEW_SPACING}px; 
            scrollbar: false; 
            border: 0px; 
        }}
        
        element {{ 
            padding: {s.ELEMENT_PADDING_VERTICAL}px {s.ELEMENT_PADDING_HORIZONTAL}px; 
            border-radius: {s.ELEMENT_BORDER_RADIUS}px; 
        }}
        
        element selected {{ 
            border: 0 0 0 2px; 
            border-color: {s.ACCENT_COLOR}; 
            border-radius: 0px; 
        }}
        
        element-icon {{ {icon_css} }}
        
        element-text {{ 
            vertical-align: 0.5; 
            markup: true; 
            expand: true; 
        }}
    """

def show_menu(node: framework.Parent, path_names: List[str] | None = None):
    actual_path = path_names or []
    selected_index = 0
    while True:
        items = node.get_children()
        is_inside_wallpapers = "Wallpapers" in actual_path
        show_icons = is_inside_wallpapers and any(i.icon and ("/" in i.icon or "." in i.icon) for i in items)

        menu_lines = []
        for i in items:
            name_part = i.render()
            item_color = getattr(i, 'color', None)
            if item_color:
                color_val = "#ffff00" if item_color == "yellow" else item_color
                name_part = f"<span foreground='{color_val}'>{name_part}</span>"

            if node.name == "Search" and i.icon and ("/" in i.icon or "." in i.icon):
                line = f"{name_part}\t<span alpha='50%' foreground='{STYLE.SECONDARY_TEXT_COLOR}' size='small'>{i.icon}</span>"
            else:
                line = name_part

            if show_icons and i.icon:
                line += f"\0icon\x1f{i.icon}"
            menu_lines.append(line)

        theme = build_rofi_theme(
            lines=min(len(items) if len(items) > 0 else 1, STYLE.get_lines_limit(node.name)), 
            has_search=node.search, 
            width=STYLE.get_width(node.name), 
            show_icons=show_icons
        )

        cmd = ["rofi", "-dmenu", "-markup-rows", "-i", "-p", actual_path[-1] if actual_path else "System", "-theme-str", theme,
               "-selected-row", str(selected_index),
               "-kb-move-char-back", "", "-kb-move-char-forward", "", "-kb-custom-1", "Left", "-kb-accept-entry", "Return,KP_Enter,Right"]

        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        stdout, _ = proc.communicate(input="\n".join(menu_lines))

        if proc.returncode in [1, -1] or not stdout:
            return "EXIT"
        if proc.returncode == 10:
            return "BACK"

        sel = clean_selection_name(stdout.strip())
        
        target = None
        for idx, item in enumerate(items):
            if item.name == sel:
                target = item
                selected_index = idx
                break
        
        if not target:
            continue

        if isinstance(target, framework.Parent):
            if show_menu(target, actual_path + [target.name]) == "EXIT":
                return "EXIT"
        elif isinstance(target, framework.Action):
            if target.execute():
                return "EXIT"
        elif isinstance(target, framework.Toggle):
            target.toggle()
            continue

def get_waybar_node(waybar_mod):
    def make_t(name, symlink, folder_path, ext):
        f = waybar_mod.WAYBAR_THEMES_DIR / folder_path
        return framework.Toggle(
            name=name, icon="",
            states=waybar_mod.get_files_in(f, ext),
            get_state=lambda: waybar_mod.get_current_stem(symlink),
            set_state=lambda s: waybar_mod.set_symlink(f, s, ext, symlink)
        )

    return framework.Parent("Waybar", icon="󰍜", children=[
        framework.Parent("Panel settings", icon="", children=[
            make_t("Monitors", "panel-monitors.jsonc", "panel/monitors", ".jsonc"),
            make_t("Color", "panel-color.css", "panel/colors", ".css"),
            make_t("Position", "panel-position.jsonc", "panel/positions", ".jsonc"),
            framework.Parent("Presets", icon="", search=True, children=lambda: [
                framework.Action(
                    name=preset_name,
                    command=lambda x=preset_name: waybar_mod.set_preset(x)
                )
                for preset_name in waybar_mod.get_preset_names()
            ])
        ]),
    ])

if __name__ == "__main__":
    from modules.apps import apps
    from modules.music import utils, radio, yandex_music
    from modules.appearance import wallpapers, waybar

    def get_root_nodes():
        items = []
        if utils.is_playing():
            items.append(framework.Action("Stop Music", icon="󰓛", command=utils.stop_music_logic))

        items.extend([
            framework.Parent("Apps", icon="󰀻", search=True, children=apps.get_nodes()),
            framework.Parent("Music", icon="", children=[
                framework.Action("Yandex Music", yandex_music.run_music, icon="", exit=True),
                framework.Parent("Radio", icon="", search=True, children=radio.get_nodes())
            ]),
            framework.Parent("Appearance", icon="", children=[
                framework.Parent("Wallpapers", icon="", search=True, children=wallpapers.get_nodes()),
                get_waybar_node(waybar)
            ]),
            framework.Parent("Maintenance", icon="󰒓", children=[
                framework.Action("Systemd manager", "kitty --hold -e systemd-manager-tui", icon="", exit=True),
                framework.Action("Installed packages", f"kitty -e {SCRIPTS_DIR}/installed_packages.sh", icon="", exit=True),
                framework.Action("System health", f"kitty -e {SCRIPTS_DIR}/system_health.py", icon="", exit=True),
                framework.Action("Asus Center", f"kitty -e sudo {SCRIPTS_DIR}/asus_center.py", icon="󰊖", exit=True),
                framework.Action("Update system", f"kitty -e sudo {SCRIPTS_DIR}/update_system.py", icon="", exit=True),
                framework.Action("Clean cache", f"kitty -e sudo {SCRIPTS_DIR}/clean_cache.py", icon="󰃢", exit=True),
                framework.Action("Backups manager", f"kitty -e sudo {SCRIPTS_DIR}/backup_manager.py", icon="", exit=True)
            ]),
            framework.Parent("Capture", icon="", children=[
                framework.Action("Record screen", f"{SCRIPTS_DIR}/record_screen.sh", icon="", exit=True),
                framework.Action("Full screenshot", f"{SCRIPTS_DIR}/make_full_screenshot.sh", icon="", exit=True),
            ]),
            framework.Parent("Power menu", icon="", children=[
                framework.Action("Lock", "hyprlock", icon="", exit=True),
                framework.Action("Logout", "hyprctl dispatch exit", icon="󰍃", exit=True),
                framework.Action("Reboot", "systemctl reboot", icon="󰑓", exit=True),
                framework.Action("Poweroff", "systemctl poweroff", icon="󰚦", exit=True),
            ])
        ])
        return items

    show_menu(framework.Parent("Main", children=get_root_nodes, search=False))

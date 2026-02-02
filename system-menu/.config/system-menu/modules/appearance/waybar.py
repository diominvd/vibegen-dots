import os
import subprocess
from pathlib import Path

HOME = Path.home()
WAYBAR_THEMES_DIR = HOME / ".config/waybar/themes"
WAYBAR_COMPONENTS_DIR = HOME / ".config/waybar/components"
WAYBAR_SCRIPTS_DIR = HOME / ".config/waybar/scripts"

def restart_waybar():
    """Fully restart waybar (kill and start)."""
    try:
        # Kill waybar
        subprocess.run(["pkill", "waybar"], stderr=subprocess.DEVNULL)
        # Wait a bit to ensure it's dead
        subprocess.run(["sleep", "0.1"])
        # Start waybar in background
        subprocess.Popen(["waybar"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error restarting waybar: {e}")

def set_symlink(folder: Path, file_stem: str, extension: str, symlink_target: str):
    """Create symlink for a single file."""
    source = folder / f"{file_stem}{extension}"
    target = WAYBAR_COMPONENTS_DIR / symlink_target
    try:
        if target.exists() or target.is_symlink():
            target.unlink()
        target.symlink_to(source)
        restart_waybar()
    except Exception as e:
        print(f"Waybar error: {e}")

def set_preset(preset_name: str):
    """
    Set a preset: create symlinks for config, styles, and scripts.
    
    Creates:
    - components/panel-preset.jsonc -> themes/panel/presets/{preset_name}/{preset_name}.jsonc
    - components/widgets-style.css -> themes/panel/presets/{preset_name}/{preset_name}.css
    - scripts/ -> themes/panel/presets/{preset_name}/scripts/
    """
    preset_dir = WAYBAR_THEMES_DIR / "panel/presets" / preset_name
    
    if not preset_dir.exists():
        print(f"Preset directory not found: {preset_dir}")
        return
    
    try:
        # 1. Symlink for config (.jsonc)
        config_source = preset_dir / f"{preset_name}.jsonc"
        config_target = WAYBAR_COMPONENTS_DIR / "panel-preset.jsonc"
        
        if config_source.exists():
            if config_target.exists() or config_target.is_symlink():
                config_target.unlink()
            config_target.symlink_to(config_source)
        
        # 2. Symlink for widget styles (.css)
        style_source = preset_dir / f"{preset_name}.css"
        style_target = WAYBAR_COMPONENTS_DIR / "widgets-style.css"
        
        if style_source.exists():
            if style_target.exists() or style_target.is_symlink():
                style_target.unlink()
            style_target.symlink_to(style_source)
        
        # 3. Symlink for scripts folder
        scripts_source = preset_dir / "scripts"
        
        if scripts_source.exists() and scripts_source.is_dir():
            if WAYBAR_SCRIPTS_DIR.exists() or WAYBAR_SCRIPTS_DIR.is_symlink():
                if WAYBAR_SCRIPTS_DIR.is_symlink():
                    WAYBAR_SCRIPTS_DIR.unlink()
                else:
                    # Backup existing directory if it's not a symlink
                    backup_dir = WAYBAR_SCRIPTS_DIR.parent / "scripts.backup"
                    if backup_dir.exists():
                        subprocess.run(["rm", "-rf", str(backup_dir)])
                    WAYBAR_SCRIPTS_DIR.rename(backup_dir)
            
            WAYBAR_SCRIPTS_DIR.symlink_to(scripts_source)
        
        # Restart waybar completely
        restart_waybar()
        
    except Exception as e:
        print(f"Error setting preset '{preset_name}': {e}")

def get_current_stem(symlink_target: str) -> str:
    """Read current state from symlink."""
    target = WAYBAR_COMPONENTS_DIR / symlink_target
    if target.exists() and target.is_symlink():
        return Path(os.readlink(target)).stem
    return ""

def get_files_in(folder_path: Path, extension: str):
    """Return list of file stems for Action."""
    if not folder_path.exists():
        return []
    return [f.stem for f in sorted(folder_path.glob(f"*{extension}"))]

def get_preset_names():
    """Get all available preset names (directories in panel/presets/)."""
    presets_dir = WAYBAR_THEMES_DIR / "panel/presets"
    
    if not presets_dir.exists():
        return []
    
    return [
        d.name 
        for d in sorted(presets_dir.iterdir()) 
        if d.is_dir() and not d.name.startswith('.')
    ]

def get_current_preset() -> str:
    """Get currently active preset name."""
    config_link = WAYBAR_COMPONENTS_DIR / "panel-preset.jsonc"
    
    if config_link.exists() and config_link.is_symlink():
        # Get the preset name from the symlink path
        # e.g., /home/user/.config/waybar/themes/panel/presets/boxes/boxes.jsonc
        target = Path(os.readlink(config_link))
        return target.parent.name
    
    return ""

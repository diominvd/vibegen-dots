#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess
import glob
from pathlib import Path
from typing import List, Tuple

# ==============================================================================
# ENVIRONMENT COMPATIBILITY (HYPRLAND / WAYLAND)
# ==============================================================================
os.environ["XDG_CURRENT_DESKTOP"] = "Sway"
os.environ["GTK_USE_PORTAL"] = "0"

# ==============================================================================
# CONFIGURATION & COLORS
# ==============================================================================
class Colors:
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"   # Safe
    YELLOW = "\033[93m"  # Warning
    RED = "\033[91m"     # Dangerous
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

LEVEL_SAFE = "SAFE"
LEVEL_WARNING = "WARNING"
LEVEL_DANGEROUS = "DANGEROUS"

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def clear_screen():
    """Clears the terminal screen."""
    subprocess.run(['clear' if os.name == 'posix' else 'cls'])

def get_dir_size(path: str) -> int:
    """Calculates the total size of a directory in bytes."""
    total_size = 0
    try:
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    except Exception:
        pass
    return total_size

def format_bytes(size: float) -> str:
    """Converts bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def run_command(cmd: List[str]) -> Tuple[bool, str]:
    """Runs a shell command and returns success status and output."""
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return (result.returncode == 0, result.stdout.strip())
    except Exception as e:
        return (False, str(e))

def print_header():
    """Displays the stylized ASCII branding."""
    art = f"""{Colors.CYAN}{Colors.BOLD}
 ██████╗██╗      ███████╗ █████╗ ███╗    ██╗██╗███╗    ██╗ ██████╗      ██████╗ █████╗  ██████╗██╗  ██╗███████╗
██╔════╝██║      ██╔════╝██╔══██╗████╗  ██║██║████╗  ██║██╔════╝      ██╔════╝██╔══██╗██╔════╝██║  ██║██╔════╝
██║      ██║      █████╗  ███████║██╔██╗ ██║██║██╔██╗ ██║██║  ███╗     ██║      ███████║██║      ███████║█████╗  
██║      ██║      ██╔══╝  ██╔══██║██║╚██╗██║██║██║╚██╗██║██║   ██║     ██║      ██╔══██║██║      ██╔══██║██╔══╝  
╚██████╗███████╗███████╗██║  ██║██║ ╚████║██║██║ ╚████║╚██████╔╝     ╚██████╗██║  ██║╚██████╗██║  ██║███████╗
 ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝      ╚═════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝
{Colors.RESET}"""
    print(art)
    print(f"{Colors.BLUE}{'='*110}{Colors.RESET}")
    print(f"{Colors.BOLD}    CLEANING CACHE MANAGER — PROFESSIONAL EDITION{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*110}{Colors.RESET}\n")

# ==============================================================================
# CLEANING TASK CLASSES
# ==============================================================================
class CleanTask:
    def __init__(self, name: str, description: str, safety: str):
        self.name = name
        self.description = description
        self.safety = safety
        self.size_bytes = 0
        self.items_count = 0

    def analyze(self): raise NotImplementedError
    def clean(self): raise NotImplementedError

    def get_color(self):
        if self.safety == LEVEL_SAFE: return Colors.GREEN
        if self.safety == LEVEL_WARNING: return Colors.YELLOW
        if self.safety == LEVEL_DANGEROUS: return Colors.RED
        return Colors.RESET

class PacmanCacheTask(CleanTask):
    def __init__(self):
        super().__init__("Pacman Cache", "Removes all downloaded packages in /var/cache/pacman/pkg/", LEVEL_WARNING)
        self.cache_path = "/var/cache/pacman/pkg/"
    def analyze(self):
        if os.path.exists(self.cache_path):
            self.size_bytes = get_dir_size(self.cache_path)
            self.items_count = len(os.listdir(self.cache_path))
    def clean(self):
        subprocess.run(["pacman", "-Scc", "--noconfirm"])

class OrphansTask(CleanTask):
    def __init__(self):
        super().__init__("Orphan Packages", "Unused dependencies (pacman -Qtdq)", LEVEL_SAFE)
        self.orphans = []
    def analyze(self):
        success, output = run_command(["pacman", "-Qtdq"])
        if success and output:
            self.orphans = output.split('\n')
            self.items_count = len(self.orphans)
    def clean(self):
        if self.orphans:
            subprocess.run(["pacman", "-Rns", "--noconfirm"] + self.orphans)

class UserCacheTask(CleanTask):
    def __init__(self):
        super().__init__("User Caches", "Contents of ~/.cache/", LEVEL_SAFE)
        self.targets = []
    def analyze(self):
        home_dirs = glob.glob("/home/*")
        for home in home_dirs:
            cache_dir = os.path.join(home, ".cache")
            if os.path.exists(cache_dir):
                self.targets.append(cache_dir)
                self.size_bytes += get_dir_size(cache_dir)
                self.items_count += len(os.listdir(cache_dir))
    def clean(self):
        skip_list = ["nvim", "browser_extensions_cache"]
        for target in self.targets:
            for item in os.listdir(target):
                item_path = os.path.join(target, item)
                if any(skip_item in item for skip_item in skip_list): continue
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path): os.unlink(item_path)
                    elif os.path.isdir(item_path): shutil.rmtree(item_path)
                except Exception: pass

class JournalTask(CleanTask):
    def __init__(self):
        super().__init__("Systemd Journal", "Logs older than 2 weeks", LEVEL_SAFE)
    def analyze(self):
        if os.path.exists("/var/log/journal"):
            self.size_bytes = get_dir_size("/var/log/journal")
    def clean(self):
        subprocess.run(["journalctl", "--vacuum-time=2weeks"])

# ==============================================================================
# MAIN LOGIC
# ==============================================================================
def main():
    if os.geteuid() != 0:
        print(f"{Colors.RED}❌ Error: This script must be run as root (sudo).{Colors.RESET}")
        sys.exit(1)

    tasks: List[CleanTask] = [PacmanCacheTask(), OrphansTask(), UserCacheTask(), JournalTask()]

    while True:
        clear_screen()
        print_header()
        
        print(f"{Colors.BOLD}{'#':<3} {'Safety':<10} {'Task Name':<20} {'Size':<12} {'Description'}{Colors.RESET}")
        print(f"{Colors.DIM}{'-' * 110}{Colors.RESET}")

        total_reclaimable = 0
        for i, task in enumerate(tasks):
            task.analyze()
            total_reclaimable += task.size_bytes
            color = task.get_color()
            print(f"{i+1:<3} {color}{task.safety:<10}{Colors.RESET} {task.name:<20} {format_bytes(task.size_bytes):<12} {task.description}")

        print(f"{Colors.DIM}{'-' * 110}{Colors.RESET}")
        print(f"{Colors.BOLD}Total estimated space to reclaim: {Colors.GREEN}{format_bytes(total_reclaimable)}{Colors.RESET}\n")

        print(f"{Colors.BOLD}Enter task numbers (e.g., '1 2'), 'all' to clean everything, or '0' to exit.{Colors.RESET}")
        choice = input(f"{Colors.CYAN}Selection: {Colors.RESET}").strip().lower()

        if choice == '0' or choice == 'q': break
        
        selected_indices = []
        if choice == 'all':
            selected_indices = range(len(tasks))
        else:
            try:
                selected_indices = [int(i)-1 for i in choice.split() if 0 <= int(i)-1 < len(tasks)]
            except ValueError: continue

        if not selected_indices: continue

        confirm = input(f"\n{Colors.RED}{Colors.BOLD}⚠️  Are you sure you want to delete these files? (y/N): {Colors.RESET}").lower()
        if confirm == 'y':
            for idx in selected_indices:
                task = tasks[idx]
                print(f"\n{Colors.YELLOW}>>> Running: {task.name}...{Colors.RESET}")
                task.clean()
            print(f"\n{Colors.GREEN}✅ Cleanup Complete!{Colors.RESET}")
            input(f"\n{Colors.DIM}Press ENTER to continue...{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interrupted. Exiting safely...{Colors.RESET}")

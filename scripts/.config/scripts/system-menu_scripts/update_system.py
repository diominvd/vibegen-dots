#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import sys

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
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

# ==============================================================================
# CORE FUNCTIONS
# ==============================================================================
def clear_screen():
    """Clears the terminal screen."""
    subprocess.run(['clear' if os.name == 'posix' else 'cls'])

def print_header():
    """Displays the stylized ASCII branding."""
    art = f"""{Colors.CYAN}{Colors.BOLD}
██╗   ██╗██████╗ ██████╗  █████╗ ████████╗██╗███╗   ██╗ ██████╗      ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗
██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║████╗  ██║██╔════╝      ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║
██║   ██║██████╔╝██║  ██║███████║   ██║   ██║██╔██╗ ██║██║  ███╗     ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║
██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██║██║╚██╗██║██║   ██║     ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║
╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ██║██║ ╚████║╚██████╔╝     ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║
 ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝      ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝
{Colors.RESET}"""
    print(art)
    print(f"{Colors.BLUE}{'='*120}{Colors.RESET}")
    print(f"{Colors.BOLD}    SYSTEM UPDATE MANAGER — PROFESSIONAL EDITION{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*120}{Colors.RESET}\n")

def update_pacman():
    """Updates official repositories using pacman."""
    print(f"\n{Colors.BOLD}[1] Updating Official Repositories (pacman)...{Colors.RESET}")
    res = subprocess.run(["sudo", "pacman", "-Syu", "--noconfirm"])
    if res.returncode == 0:
        print(f"{Colors.GREEN}✅ Pacman update successful.{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ Error during Pacman update.{Colors.RESET}")

def update_aur():
    """Updates AUR packages using yay."""
    print(f"\n{Colors.BOLD}[2] Updating AUR Packages (yay)...{Colors.RESET}")
    res = subprocess.run(["yay", "-Sua", "--noconfirm"])
    if res.returncode == 0:
        print(f"{Colors.GREEN}✅ AUR update successful.{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ Error during AUR update.{Colors.RESET}")

# ==============================================================================
# MAIN MENU
# ==============================================================================
def main():
    while True:
        clear_screen()
        print_header()
        
        print(f"{Colors.BOLD}SELECT UPDATE ACTION:{Colors.RESET}")
        print(f"{Colors.CYAN}1){Colors.RESET} Update Pacman (Official Repos)")
        print(f"{Colors.CYAN}2){Colors.RESET} Update AUR (Yay)")
        print(f"{Colors.CYAN}3){Colors.RESET} Full System Update (Both)")
        print(f"{Colors.RED}0){Colors.RESET} Exit")
        
        choice = input(f"\n{Colors.BOLD}Action: {Colors.RESET}").strip()
        
        if choice == '1':
            update_pacman()
        elif choice == '2':
            update_aur()
        elif choice == '3':
            update_pacman()
            update_aur()
        elif choice == '0':
            print(f"{Colors.YELLOW}Exiting update manager...{Colors.RESET}")
            break
        else:
            continue
            
        input(f"\n{Colors.DIM}Press ENTER to return to menu...{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}Interrupted by user. Exiting...{Colors.RESET}")
        sys.exit(0)

#!/usr/bin/env python3
import subprocess
import os
from datetime import datetime

# ==============================================================================
# ENVIRONMENT FIX FOR HYPRLAND / ROFI
# ==============================================================================
# These variables bypass the XDG Desktop Portal settings check that often 
# fails when launching GUI-linked scripts via Rofi in Hyprland.
# Using "Sway" acts as a compatibility mode for wlroots-based compositors.
os.environ["XDG_CURRENT_DESKTOP"] = "Sway"
os.environ["GTK_USE_PORTAL"] = "0"

# ==============================================================================
# CONFIGURATION
# ==============================================================================
# Path to your Borg repository. Ensure the user has sudo/write access.
REPO = "/backup/borg-repo"

# ANSI Escape Sequences for terminal styling
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

def clear_screen():
    """
    Clears the terminal screen using subprocess.run for better compatibility.
    """
    subprocess.run(['clear' if os.name == 'posix' else 'cls'])

def print_header():
    """
    Displays the application branding and ASCII art.
    """
    art = f"""{CYAN}{BOLD}
 ██████╗██████╗ ███████╗ █████╗ ████████╗██╗███╗   ██╗ ██████╗     ██████╗  █████╗  ██████╗██╗  ██╗██╗   ██╗██████╗ 
██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██║████╗  ██║██╔════╝     ██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██║   ██║██╔══██╗
██║     ██████╔╝█████╗  ███████║   ██║   ██║██╔██╗ ██║██║  ███╗    ██████╔╝███████║██║     █████╔╝ ██║   ██║██████╔╝
██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██║██║╚██╗██║██║   ██║    ██╔══██╗██╔══██║██║     ██╔═██╗ ██║   ██║██╔═══╝ 
╚██████╗██║  ██║███████╗██║  ██║   ██║   ██║██║ ╚████║╚██████╔╝    ██████╔╝██║  ██║╚██████╗██║  ██╗╚██████╔╝██║     
 ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     
{RESET}"""
    print(art)
    print(f"{BLUE}{'='*80}{RESET}")
    print(f"{BOLD}    BORG BACKUP MANAGER (HYPRLAND EDITION){RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")

def run_cmd(cmd_list):
    """
    Execution wrapper for system commands using subprocess.
    """
    try:
        subprocess.run(cmd_list, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n{RED}❌ Command failed with return code {e.returncode}{RESET}")
    except FileNotFoundError:
        print(f"\n{RED}❌ Error: 'borg' or 'sudo' not found in system path.{RESET}")

def create_backup():
    """
    Creates a new compressed Borg archive of the system directories.
    """
    print(f"\n{GREEN}>>> Starting backup creation...{RESET}")
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    archive = f"{REPO}::system-{timestamp}"
    
    cmd = [
        "sudo", "borg", "create", "--progress", "--stats", "--compression", "lz4",
        "--exclude", "/dev", "--exclude", "/proc", "--exclude", "/sys",
        "--exclude", "/tmp", "--exclude", "/run", "--exclude", "/mnt",
        "--exclude", "/media", "--exclude", "/lost+found", "--exclude", "/timeshift",
        "--exclude", "/backup", "--exclude", "/home", "--exclude", "/var/cache",
        "--exclude", "/var/tmp", "--exclude", "/var/log",
        archive, "/boot", "/etc", "/root", "/opt", "/usr/local", "/var"
    ]
    
    run_cmd(cmd)
    print(f"\n{GREEN}✅ Archive created: {archive}{RESET}")
    print(f"\n{BOLD}Root Partition Stats:{RESET}")
    run_cmd(["df", "-h", "/"])

def list_backups():
    """Lists all available archives in the defined repository."""
    print(f"\n{YELLOW}>>> Current Archive List:{RESET}")
    run_cmd(["sudo", "borg", "list", REPO])

def main():
    """
    Primary application loop.
    """
    while True:
        clear_screen()
        print_header()
        
        print(f"{BOLD}Main Menu:{RESET}")
        print(f"{CYAN}1){RESET} Create Backup")
        print(f"{CYAN}2){RESET} List Archives")
        print(f"{CYAN}3){RESET} Integrity Check")
        print(f"{CYAN}4){RESET} Repository Info")
        print(f"{RED}0){RESET} Exit")
        
        try:
            choice = input(f"\n{BOLD}Action: {RESET}").strip()
        except EOFError:
            break
            
        if choice == '1':
            create_backup()
        elif choice == '2':
            list_backups()
        elif choice == '3':
            print(f"\n{YELLOW}>>> Running 'borg check' (Integrity Check)...{RESET}")
            run_cmd(["sudo", "borg", "check", "--progress", REPO])
        elif choice == '4':
            print(f"\n{YELLOW}>>> Repository Statistics:{RESET}")
            run_cmd(["sudo", "borg", "info", REPO])
            run_cmd(["df", "-h", "/"])
        elif choice == '0':
            print("Exiting Manager. Goodbye.")
            break
        
        input(f"\n{DIM}Press ENTER to return to menu...{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Interrupted. Exiting safely...{RESET}")

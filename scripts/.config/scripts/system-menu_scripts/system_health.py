#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import sys
import time
import re

# ==============================================================================
# ENVIRONMENT COMPATIBILITY
# ==============================================================================
os.environ["XDG_CURRENT_DESKTOP"] = "Sway"
os.environ["GTK_USE_PORTAL"] = "0"

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
# FIXING THE BUG: ROBUST TEMP PARSING
# ==============================================================================
def get_cpu_temp():
    """Fetches CPU temperature using regex to avoid ValueError."""
    try:
        # Try lm-sensors first
        sensors_data = subprocess.check_output(["sensors"], text=True)
        # Looking for lines like 'Package id 0:  +50.0°C' or 'Core 0: +45.0°C'
        match = re.search(r'(?:Package id 0|Core 0|Tctl):\s+\+?([\d.]+)', sensors_data)
        if match:
            return float(match.group(1))
    except:
        pass
    
    try:
        # Fallback to thermal_zone
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return float(f.read()) / 1000
    except:
        return None

def get_gpu_info():
    """Fetches NVIDIA GPU temperature if available."""
    try:
        out = subprocess.check_output(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"], text=True)
        return out.strip() + "°C"
    except:
        return "N/A"

def get_energy_rate():
    try:
        raw_data = subprocess.check_output(["upower", "-i", "/org/freedesktop/UPower/devices/battery_BAT0"], text=True)
    except Exception:
        raw_data = subprocess.check_output(["upower", "-b"], text=True)
    stats = {
        line.split(":", 1)[0].strip(): line.split(":", 1)[1].strip()
        for line in raw_data.splitlines()
        if ":" in line
    }
    return stats.get("energy-rate", "N/A")

def get_ram_usage():
    try:
        out = subprocess.check_output(["free", "-m"], text=True).split('\n')[1].split()
        total, used = int(out[1]), int(out[2])
        percent = (used / total) * 100
        return f"{used}MB / {total}MB ({percent:.1f}%)", percent
    except:
        return "N/A", 0

def get_disk_usage():
    try:
        out = subprocess.check_output(["df", "-h", "/"], text=True).split('\n')[1].split()
        return f"{out[2]} / {out[1]} ({out[4]})", int(out[4].replace("%", ""))
    except:
        return "N/A", 0

# ==============================================================================
# UI COMPONENTS
# ==============================================================================
def print_header():
    art = f"""{Colors.CYAN}{Colors.BOLD}
 ██████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗    ██╗  ██╗███████╗ █████╗ ██╗     ████████╗██╗  ██╗
██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║    ██║  ██║██╔════╝██╔══██╗██║     ╚══██╔══╝██║  ██║
╚█████╗  ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║    ███████║█████╗  ███████║██║        ██║   ███████║
 ╚═══██╗  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║    ██╔══██║██╔══╝  ██╔══██║██║        ██║   ██╔══██║
██████╔╝   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║    ██║  ██║███████╗██║  ██║███████╗   ██║   ██║  ██║
╚═════╝    ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝
{Colors.RESET}"""
    print(art)
    print(f"{Colors.BLUE}{'='*110}{Colors.RESET}")
    print(f"{Colors.BOLD}    SYSTEM HEALTH & LIVE MONITOR — ARCH LINUX EDITION{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*110}{Colors.RESET}\n")

def display_dashboard():
    temp = get_cpu_temp()
    gpu_temp = get_gpu_info()
    energy_rate = get_energy_rate()
    ram_str, ram_pct = get_ram_usage()
    disk_str, disk_pct = get_disk_usage()
    
    try:
        uptime = subprocess.check_output(["uptime", "-p"], text=True).strip().replace("up ", "")
    except:
        uptime = "N/A"

    # Color Logic
    temp_display = f"{temp}°C" if temp is not None else "N/A"
    temp_color = Colors.RED if (temp and temp > 75) else Colors.GREEN
    ram_color = Colors.YELLOW if ram_pct > 80 else Colors.GREEN
    disk_color = Colors.RED if disk_pct > 90 else Colors.GREEN

    print(f"{Colors.BOLD}STATISTICS:{Colors.RESET}")
    print(f"  {Colors.CYAN}Uptime:        {Colors.RESET}{uptime}")
    print(f"  {Colors.CYAN}CPU Temp:      {temp_color}{temp_display}{Colors.RESET}")
    print(f"  {Colors.CYAN}GPU Temp:      {Colors.GREEN}{gpu_temp}{Colors.RESET}")
    print(f"  {Colors.CYAN}Energy Rate:   {Colors.GREEN}{energy_rate}{Colors.RESET}")
    print(f"  {Colors.CYAN}RAM Usage:     {ram_color}{ram_str}{Colors.RESET}")
    print(f"  {Colors.CYAN}Disk Root:     {disk_color}{disk_str}{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}QUICK ACTIONS:{Colors.RESET}")
    print(f"  {Colors.BLUE}1){Colors.RESET} Open htop           {Colors.BLUE}2){Colors.RESET} Open btop")
    print(f"  {Colors.BLUE}3){Colors.RESET} Check Failed Logs   {Colors.BLUE}4){Colors.RESET} Systemd Errors")
    print(f"  {Colors.RED}0){Colors.RESET} Exit")

def main():
    while True:
        os.system('clear')
        print_header()
        display_dashboard()
        
        try:
            choice = input(f"\n{Colors.BOLD}Select Action (or Enter to Refresh): {Colors.RESET}").strip()
        except EOFError: break
        
        if choice == '1': subprocess.run(["htop"])
        elif choice == '2': subprocess.run(["btop"])
        elif choice == '3': os.system("journalctl -p 3 -xb | less")
        elif choice == '4': os.system("systemctl --failed | less")
        elif choice == '0': break
        else: continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)

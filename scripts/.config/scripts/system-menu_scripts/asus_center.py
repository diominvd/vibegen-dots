#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess
import time
from typing import List, Tuple

# ==============================================================================
# CONFIGURATION & COLORS
# ==============================================================================
class Colors:
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"   # Safe/Low power
    YELLOW = "\033[93m"  # Warning/Medium
    RED = "\033[91m"     # Dangerous/High performance
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    MAGENTA = "\033[95m"

LEVEL_LOW_POWER = "LOW_POWER"
LEVEL_BALANCED = "BALANCED"
LEVEL_HIGH_PERF = "HIGH_PERF"

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def clear_screen():
    """Clears the terminal screen."""
    subprocess.run(['clear' if os.name == 'posix' else 'cls'])

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
 █████╗ ███████╗██╗   ██╗███████╗    ██████╗  ██████╗  ██████╗     ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ 
██╔══██╗██╔════╝██║   ██║██╔════╝    ██╔══██╗██╔═══██╗██╔════╝     ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗
███████║███████╗██║   ██║███████╗    ██████╔╝██║   ██║██║  ███╗    ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝
██╔══██║╚════██║██║   ██║╚════██║    ██╔══██╗██║   ██║██║   ██║    ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗
██║  ██║███████║╚██████╔╝███████║    ██║  ██║╚██████╔╝╚██████╔╝    ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
{Colors.RESET}"""
    print(art)
    print(f"{Colors.BLUE}{'='*130}{Colors.RESET}")
    print(f"{Colors.BOLD}    HARDWARE CONFIGURATION MANAGER — PROFESSIONAL EDITION{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*130}{Colors.RESET}\n")

# ==============================================================================
# CONTROL MODULE CLASSES
# ==============================================================================
class ControlModule:
    """Base class for all hardware control modules."""
    def __init__(self, name: str, description: str, category: str):
        self.name = name
        self.description = description
        self.category = category
        self.current_state = "Unknown"
        self.available_options = []

    def analyze(self): 
        """Refresh current hardware state."""
        raise NotImplementedError
    
    def configure(self): 
        """Interactive configuration menu."""
        raise NotImplementedError

    def get_color(self):
        """Returns color based on current state."""
        s = self.current_state.lower()
        # High performance states
        if any(x in s for x in ["perf", "dedicated", "3", "high", "100%", "max"]): 
            return Colors.RED
        # Low power states
        if any(x in s for x in ["quiet", "integrated", "silent", "0", "off", "60%", "level 0"]): 
            return Colors.GREEN
        # Balanced/Medium states
        return Colors.YELLOW

class PowerProfileModule(ControlModule):
    def __init__(self):
        super().__init__(
            "Power Profile", 
            "CPU/Fan performance mode", 
            LEVEL_BALANCED
        )
        self.available_options = ["Quiet", "Balanced", "Performance"]

    def analyze(self):
        """Get current power profile."""
        # Новый синтаксис (v5+)
        success, output = run_command(["asusctl", "profile", "get"])
        if success and output:
            # Парсим вывод: "Active profile: Balanced"
            for line in output.split('\n'):
                if "Active profile:" in line:
                    profile = line.split("Active profile:")[-1].strip()
                    if profile in ["Quiet", "Balanced", "Performance"]:
                        self.current_state = profile
                        return
        
        # Альтернатива: через list (показывает все профили)
        success, output = run_command(["asusctl", "profile", "list"])
        if success and output:
            # В новых версиях активный профиль может быть помечен
            lines = output.strip().split('\n')
            for line in lines:
                # Ищем маркер активного профиля (может быть *, > или подобное)
                if any(marker in line for marker in ['*', '>', '•']):
                    for profile in ["Quiet", "Balanced", "Performance"]:
                        if profile in line:
                            self.current_state = profile
                            return
        
        # Старый синтаксис (v4)
        success, output = run_command(["asusctl", "profile", "-p"])
        if success and output:
            words = output.strip().split()
            for word in words:
                word_clean = word.strip('*').strip()
                if word_clean in ["Quiet", "Balanced", "Performance"]:
                    self.current_state = word_clean
                    return
        
        # Последняя попытка через platform_profile
        if os.path.exists("/sys/firmware/acpi/platform_profile"):
            try:
                with open("/sys/firmware/acpi/platform_profile", 'r') as f:
                    profile = f.read().strip()
                    mapping = {
                        "low-power": "Quiet",
                        "balanced": "Balanced",
                        "performance": "Performance"
                    }
                    self.current_state = mapping.get(profile, profile.capitalize())
                    return
            except:
                pass
        
        self.current_state = "Unknown"

    def configure(self):
        """Change power profile."""
        print(f"\n{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.BOLD}Power Profile Configuration{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*80}{Colors.RESET}\n")
        
        print(f"{Colors.GREEN}1.{Colors.RESET} Quiet      - Minimal fan noise, lower performance (battery saving)")
        print(f"{Colors.YELLOW}2.{Colors.RESET} Balanced   - Optimal balance between performance and noise")
        print(f"{Colors.RED}3.{Colors.RESET} Performance - Maximum performance, increased fan speed\n")
        
        print(f"{Colors.DIM}Current: {self.get_color()}{self.current_state}{Colors.RESET}\n")
        
        sel = input(f"{Colors.CYAN}Selection (1-3, or 0 to cancel): {Colors.RESET}").strip()
        
        mapping = {"1": "Quiet", "2": "Balanced", "3": "Performance"}
        if sel in mapping:
            profile = mapping[sel]
            
            # Новый синтаксис (v5+): asusctl profile set <profile>
            success, output = run_command(["asusctl", "profile", "set", profile])
            
            # Если не сработало, пробуем старый синтаксис
            if not success:
                success, output = run_command(["asusctl", "profile", "-P", profile])
            
            if success:
                print(f"\n{Colors.GREEN}✅ Profile changed to {Colors.BOLD}{profile}{Colors.RESET}")
            else:
                print(f"\n{Colors.RED}❌ Failed to change profile{Colors.RESET}")
                if output:
                    print(f"{Colors.YELLOW}{output}{Colors.RESET}")
            time.sleep(1.5)
        elif sel != "0":
            print(f"\n{Colors.RED}Invalid selection{Colors.RESET}")
            time.sleep(1)

class GpuModeModule(ControlModule):
    def __init__(self):
        super().__init__(
            "GPU Mode", 
            "Graphics switching (requires logout)", 
            LEVEL_HIGH_PERF
        )
        self.available_options = ["Hybrid", "Integrated", "Dedicated", "Vfio"]

    def analyze(self):
        """Get current GPU mode."""
        success, output = run_command(["supergfxctl", "-g"])
        if success:
            self.current_state = output.strip().capitalize()
        else:
            self.current_state = "N/A"

    def configure(self):
        """Change GPU mode."""
        print(f"\n{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.BOLD}GPU Mode Configuration{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*80}{Colors.RESET}\n")
        
        print(f"{Colors.YELLOW}1.{Colors.RESET} Hybrid      - Automatic switching (recommended)")
        print(f"{Colors.GREEN}2.{Colors.RESET} Integrated  - Intel/AMD only (maximum battery life)")
        print(f"{Colors.RED}3.{Colors.RESET} Dedicated   - NVIDIA only (maximum performance)")
        print(f"{Colors.MAGENTA}4.{Colors.RESET} Vfio        - GPU passthrough for VMs\n")
        
        print(f"{Colors.DIM}Current: {self.get_color()}{self.current_state}{Colors.RESET}")
        print(f"{Colors.RED}{Colors.BOLD}⚠️  WARNING: Requires logout to take effect!{Colors.RESET}\n")
        
        sel = input(f"{Colors.CYAN}Selection (1-4, or 0 to cancel): {Colors.RESET}").strip()
        
        if sel.isdigit() and 1 <= int(sel) <= 4:
            mode = self.available_options[int(sel)-1].lower()
            
            confirm = input(f"\n{Colors.YELLOW}Switch to {Colors.BOLD}{mode}{Colors.RESET}{Colors.YELLOW} mode? (y/N): {Colors.RESET}").lower()
            if confirm == 'y':
                success, out = run_command(["supergfxctl", "-m", mode])
                if success:
                    print(f"\n{Colors.GREEN}✅ GPU mode set to {Colors.BOLD}{mode}{Colors.RESET}")
                    print(f"{Colors.YELLOW}⚠️  Please logout for changes to take effect{Colors.RESET}")
                else:
                    print(f"\n{Colors.RED}❌ Failed to set GPU mode{Colors.RESET}")
                time.sleep(2)
        elif sel != "0":
            print(f"\n{Colors.RED}Invalid selection{Colors.RESET}")
            time.sleep(1)

class BatteryModule(ControlModule):
    def __init__(self):
        super().__init__(
            "Battery Limit", 
            "Charge threshold for battery health", 
            LEVEL_BALANCED
        )
        self.available_options = ["60%", "80%", "100%"]

    def analyze(self):
        """Get current battery charge limit."""
        paths = [
            "/sys/class/power_supply/BAT0/charge_control_end_threshold",
            "/sys/class/power_supply/BAT1/charge_control_end_threshold",
            "/sys/class/power_supply/BATT/charge_control_end_threshold"
        ]
        
        for path in paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as f:
                        value = f.read().strip()
                        self.current_state = f"{value}%"
                        return
                except:
                    pass
        
        self.current_state = "N/A"

    def configure(self):
        """Change battery charge limit."""
        print(f"\n{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.BOLD}Battery Charge Limit Configuration{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*80}{Colors.RESET}\n")
        
        print(f"{Colors.GREEN}1.{Colors.RESET} 60%  - Maximum battery longevity (desktop/always plugged)")
        print(f"{Colors.YELLOW}2.{Colors.RESET} 80%  - Balanced health and capacity (frequently plugged)")
        print(f"{Colors.RED}3.{Colors.RESET} 100% - Full capacity (portable/unplugged use)\n")
        
        print(f"{Colors.DIM}Current: {self.get_color()}{self.current_state}{Colors.RESET}")
        print(f"{Colors.BLUE}ℹ️  Lower limits extend battery lifespan significantly{Colors.RESET}\n")
        
        sel = input(f"{Colors.CYAN}Selection (1-3, or 0 to cancel): {Colors.RESET}").strip()
        
        mapping = {"1": "60", "2": "80", "3": "100"}
        if sel in mapping:
            val = mapping[sel]
            success, output = run_command(["asusctl", "battery", "-c", val])
            if not success:
                success, output = run_command(["asusctl", "-c", val])
            
            if success:
                print(f"\n{Colors.GREEN}✅ Battery limit set to {Colors.BOLD}{val}%{Colors.RESET}")
            else:
                print(f"\n{Colors.RED}❌ Failed to set battery limit{Colors.RESET}")
            time.sleep(1.5)
        elif sel != "0":
            print(f"\n{Colors.RED}Invalid selection{Colors.RESET}")
            time.sleep(1)

class KeyboardLedModule(ControlModule):
    def __init__(self):
        super().__init__(
            "Keyboard LED", 
            "Backlight brightness level", 
            LEVEL_LOW_POWER
        )
        self.available_options = ["Off", "Low", "Medium", "High"]

    def analyze(self):
        """Get current keyboard backlight brightness."""
        paths = [
            "/sys/class/leds/asus::kbd_backlight/brightness",
            "/sys/devices/platform/asus-nb-wmi/leds/asus::kbd_backlight/brightness"
        ]
        
        for path in paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as f:
                        level = f.read().strip()
                        level_names = {
                            "0": "Off",
                            "1": "Low", 
                            "2": "Medium",
                            "3": "High"
                        }
                        self.current_state = level_names.get(level, f"Level {level}")
                        return
                except:
                    pass
        
        self.current_state = "N/A"

    def configure(self):
        """Change keyboard backlight brightness."""
        print(f"\n{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.BOLD}Keyboard Backlight Configuration{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*80}{Colors.RESET}\n")
        
        print(f"{Colors.GREEN}0.{Colors.RESET} Off    - Backlight disabled (maximum battery)")
        print(f"{Colors.CYAN}1.{Colors.RESET} Low    - Minimal brightness")
        print(f"{Colors.YELLOW}2.{Colors.RESET} Medium - Moderate brightness")
        print(f"{Colors.RED}3.{Colors.RESET} High   - Maximum brightness\n")
        
        print(f"{Colors.DIM}Current: {self.get_color()}{self.current_state}{Colors.RESET}\n")
        
        sel = input(f"{Colors.CYAN}Selection (0-3, or x to cancel): {Colors.RESET}").strip()
        
        if sel in ["0", "1", "2", "3"]:
            success, output = run_command(["asusctl", "led-mode", "-b", sel])
            
            if not success:
                paths = [
                    "/sys/class/leds/asus::kbd_backlight/brightness",
                    "/sys/devices/platform/asus-nb-wmi/leds/asus::kbd_backlight/brightness"
                ]
                
                for path in paths:
                    if os.path.exists(path):
                        try:
                            cmd = f"echo {sel} | sudo tee {path} > /dev/null"
                            result = subprocess.run(cmd, shell=True, 
                                                  stdout=subprocess.PIPE, 
                                                  stderr=subprocess.PIPE)
                            if result.returncode == 0:
                                success = True
                                break
                        except:
                            pass
            
            if success:
                level_names = {"0": "Off", "1": "Low", "2": "Medium", "3": "High"}
                print(f"\n{Colors.GREEN}✅ Brightness set to {Colors.BOLD}{level_names[sel]}{Colors.RESET}")
            else:
                print(f"\n{Colors.RED}❌ Failed to set brightness{Colors.RESET}")
                print(f"{Colors.YELLOW}💡 Tip: May require sudo permissions{Colors.RESET}")
            
            time.sleep(1.5)
        elif sel.lower() != "x":
            print(f"\n{Colors.RED}Invalid selection{Colors.RESET}")
            time.sleep(1)

# ==============================================================================
# MAIN LOGIC
# ==============================================================================
def check_dependencies():
    """Check for required utilities."""
    issues = []
    warnings = []
    info = []
    
    # Проверяем asusctl
    if not shutil.which("asusctl"):
        issues.append("asusctl not found - core functionality unavailable")
    else:
        # Проверяем версию
        success, output = run_command(["asusctl", "--version"])
        if success:
            info.append(f"asusctl version: {output}")
        
        # Проверяем демон asusd
        success, output = run_command(["systemctl", "is-active", "asusd"])
        if not success or output != "active":
            warnings.append("asusd daemon is not running - try: sudo systemctl start asusd")
    
    # Проверяем supergfxctl
    if not shutil.which("supergfxctl"):
        warnings.append("supergfxctl not found - GPU switching disabled")
    else:
        success, output = run_command(["supergfxctl", "--version"])
        if success:
            info.append(f"supergfxctl version: {output}")
    
    # Проверяем systemd (для демона)
    if not shutil.which("systemctl"):
        warnings.append("systemctl not found - cannot check service status")
    
    return issues, warnings, info

def print_dependency_status(issues, warnings, info):
    """Display dependency check results."""
    if issues:
        print(f"{Colors.RED}{'='*130}{Colors.RESET}")
        print(f"{Colors.RED}{Colors.BOLD}❌ CRITICAL: Missing Dependencies{Colors.RESET}\n")
        for issue in issues:
            print(f"  • {issue}")
        print(f"\n{Colors.YELLOW}Installation Instructions:{Colors.RESET}")
        print(f"  {Colors.CYAN}Arch/Manjaro:{Colors.RESET} yay -S asusctl supergfxctl")
        print(f"  {Colors.CYAN}Fedora:{Colors.RESET}       sudo dnf install asusctl supergfxctl")
        print(f"  {Colors.CYAN}Ubuntu:{Colors.RESET}       See https://asus-linux.org")
        print(f"{Colors.RED}{'='*130}{Colors.RESET}\n")
        return False
    
    if warnings:
        print(f"{Colors.YELLOW}⚠️  Warnings:{Colors.RESET}")
        for warning in warnings:
            print(f"  • {warning}")
        print()
    
    if info:
        print(f"{Colors.BLUE}ℹ️  System Info:{Colors.RESET}")
        for item in info:
            print(f"  • {item}")
        print()
    
    return True

def main():
    # Check dependencies
    issues, warnings, info = check_dependencies()
    
    clear_screen()
    print_header()
    
    if not print_dependency_status(issues, warnings, info):
        sys.exit(1)
    
    # Initialize all control modules
    modules: List[ControlModule] = [
        PowerProfileModule(),
        GpuModeModule(),
        BatteryModule(),
        KeyboardLedModule()
    ]

    while True:
        clear_screen()
        print_header()
        
        # Display table header
        print(f"{Colors.BOLD}{'#':<3} {'Category':<15} {'Module Name':<20} {'Current State':<20} {'Description'}{Colors.RESET}")
        print(f"{Colors.DIM}{'-' * 130}{Colors.RESET}")

        # Analyze and display each module
        for i, module in enumerate(modules):
            module.analyze()
            state_colored = f"{module.get_color()}{module.current_state:<20}{Colors.RESET}"
            
            # Category color
            cat_color = Colors.GREEN if module.category == LEVEL_LOW_POWER else \
                       Colors.YELLOW if module.category == LEVEL_BALANCED else Colors.RED
            
            print(f"{i+1:<3} {cat_color}{module.category:<15}{Colors.RESET} "
                  f"{module.name:<20} {state_colored} {module.description}")

        print(f"{Colors.DIM}{'-' * 130}{Colors.RESET}")
        
        # Command prompt
        print(f"\n{Colors.BOLD}Enter module number (1-{len(modules)}) to configure, 'r' to refresh, or '0' to exit.{Colors.RESET}")
        choice = input(f"{Colors.CYAN}Selection: {Colors.RESET}").strip().lower()

        if choice == '0' or choice == 'q':
            print(f"\n{Colors.GREEN}✅ Configuration saved. Goodbye!{Colors.RESET}\n")
            break
        
        if choice == 'r':
            continue
        
        # Handle module selection
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(modules):
                modules[idx].configure()
            else:
                print(f"\n{Colors.RED}❌ Invalid selection{Colors.RESET}")
                time.sleep(1)
        except (ValueError, IndexError):
            if choice:
                print(f"\n{Colors.RED}❌ Invalid input{Colors.RESET}")
                time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Interrupted by user. Exiting safely...{Colors.RESET}\n")
        sys.exit(0)

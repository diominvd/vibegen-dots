# vibegen-dots

<div align="center">
  <img src="assets/preview.png" width="800" alt="Hyprland Preview">
</div>

---

> [!WARNING]
> **Always back up your current configurations before installation!**
> These dotfiles are specifically designed for **Arch Linux** with the **Hyprland** Wayland compositor.

## Dependencies

To ensure a successful installation and operation of all components, you need to install the following packages.

### Prerequisites

Ensure your system is up-to-date and you have `git` and `yay` (an AUR helper) installed. If `yay` is not installed, execute the following commands:

```bash
sudo pacman -Syu # Update your system
sudo pacman -S --needed git base-devel # Install git and essential build tools
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
cd ..
rm -rf yay
```

### Package Installation

Install all required packages using `pacman` and `yay`:

```bash
# Core
sudo pacman -S wayland hyprland xdg-desktop-portal-hyprland qt5-wayland qt6-wayland stow

# UI & Appearance
sudo pacman -S waybar rofi mako swww matugen hyprlock kvantum kvantum-qt5
yay -S adw-gtk-theme ttf-jetbrains-mono-nerd

# Terminal & Shell
sudo pacman -S kitty zsh tmux starship fastfetch eza bat
yay -S oh-my-zsh-git

# Tools & Utils
sudo pacman -S neovim python python-pip ripgrep bc fzf gum thunar imv grim slurp wf-recorder wl-clipboard brightnessctl btop pacman-contrib
yay -S zed systemd-manager-tui wifitui bluetuith

# Media
sudo pacman -S mpd mpc mpd-mpris playerctl wireplumber
yay -S rmpc wiremix zen-browser-bin
```

## Installation

Follow these steps to install and set up the dotfiles.

1.  **Back up your existing configurations** (VERY IMPORTANT!)
    ```bash
    cp -r ~/.config ~/.config.backup
    cp ~/.zshrc ~/.zshrc.backup || true
    ```

2.  **Clone the dotfiles repository** to your home directory:
    ```bash
    git clone https://github.com/diominvd/vibegen-dots.git ~/.dotfiles
    cd ~/.dotfiles
    ```

3.  **Create necessary directories:**
    ```bash
    mkdir -p ~/Pictures/Wallpapers ~/Videos/Screenrecords ~/Music
    ```

4.  **Remove conflicting configurations** (this will prevent conflicts when `stow` creates symlinks):
    ```bash
    rm -rf ~/.config/{hypr,waybar,rofi,kitty,mako,fastfetch,nvim,tmux,zed,mpd,yamusic}
    rm -f ~/.zshrc
    ```

5.  **Deploy configurations with `stow`**:
    ```bash
    stow -v -t ~ fastfetch gtk-3.0 gtk-4.0 hypr kitty matugen mpd nvim rofi scripts tmux wallpapers waybar yamusic zed zsh
    ```

6.  **Set Zsh as your default shell**:
    ```bash
    chsh -s $(which zsh)
    ```

7.  **Reboot your system** and select the Hyprland session in your login manager (e.g., SDDM, GDM):
    ```bash
    reboot
    ```

### Post-Installation

After successful installation, follow these additional steps:

*   **Add Wallpapers:**
    Copy your preferred wallpapers to the `~/Pictures/Wallpapers/` directory.
    ```bash
    cp /path/to/your/wallpapers/* ~/Pictures/Wallpapers/
    # Use Super + Shift + W to apply a random wallpaper and generate the color scheme.
    ```

*   **Configure Music (MPD):**
    Copy your music files to the `~/Music/` directory.
    ```bash
    cp /path/to/your/music/* ~/Music/
    mpc update # Update the MPD database
    ```

## Keybinds

Main keybinds:

| Keybind          | Action           |
| :--------------- | :--------------- |
| `Super + Return` | Terminal         |
| `Alt + Space`    | System menu      |
| `Super + Q`      | Close window     |
| `Super + M`      | Exit Hyprland    |
| `Super + L`      | Lock screen      |

See `~/.config/hypr/config/keybinds.conf` for a full list.

## Troubleshooting

*   **Waybar not showing:**
    ```bash
    killall waybar && waybar &
    ```

*   **Colors not applying:**
    ```bash
    matugen image ~/Pictures/Wallpapers/your-wallpaper.jpg
    hyprctl reload
    ```

*   **Check logs:**
    ```bash
    journalctl -b | grep hyprland
    ```

## License

[MIT License](LICENSE)

---

<div align="center">
  **If you like this config, give it a ⭐**
</div>

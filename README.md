<div align="center">

# vibegen-dots

![Stars](https://img.shields.io/github/stars/diominvd/vibegen-dots?style=for-the-badge&color=cba6f7&logo=github)
![Forks](https://img.shields.io/github/forks/diominvd/vibegen-dots?style=for-the-badge&color=89b4fa&logo=github)
![OS](https://img.shields.io/badge/OS-Arch_Linux-icon?style=for-the-badge&logo=arch-linux&logoColor=1793D1&color=45475a)

Hyprland desktop environment with adaptive color palette based on wallpaper.

[Gallery](#gallery) • [Components](#components) • [Features](#features) • [Installation](#installation) • [Keybinds](#keybinds)

<img src="assets/preview.png" width="800" alt="Chameleon Rice Preview">

</div>

---

> [!WARNING]
> Personal configuration. Use at your own risk. Backup your configs before installation!

## Gallery

| &nbsp; | &nbsp; |
| :---: | :---: |
| <img src="assets/screenshots/scr1.jpg" width="100%"> | <img src="assets/screenshots/scr2.jpg" width="100%"> |
| <img src="assets/screenshots/scr3.jpg" width="100%"> | <img src="assets/screenshots/scr4.jpg" width="100%"> |

## Components

- **WM:** [`Hyprland`](https://hyprland.org)
- **Bar:** [`Waybar`](https://github.com/Alexays/Waybar)
- **Colors:** [`Matugen`](https://github.com/InioX/matugen)
- **Notifications:** [`Mako`](https://github.com/emersion/mako)
- **Lock:** [`Hyprlock`](https://wiki.hyprland.org/Hypr-ecosystem/hyprlock/)
- **Terminal:** [`Kitty`](https://sw.kovidgoyal.net/kitty/)
- **Shell:** [`Zsh`](https://www.zsh.org/) + [`Oh My Zsh`](https://ohmyz.sh/)
- **Launcher:** [`Rofi`](https://github.com/davatorium/rofi)

## Features

- **Adaptive colors** — System colors sync with wallpaper via Matugen
- **Advanced Rofi menu**[^1] — Apps, file search, music, wallpaper switcher, screen capture, power menu
- **TUI tools** — Minimal design with terminal-based interfaces
- **Stow management** — Easy dotfiles organization

[^1]: Use arrow keys to navigate Rofi menus

## Dependencies

<details>
<summary><b>Core</b></summary>

```bash
sudo pacman -S wayland hyprland xdg-desktop-portal-hyprland qt5-wayland qt6-wayland stow
```
</details>

<details>
<summary><b>UI & Appearance</b></summary>

```bash
sudo pacman -S waybar rofi mako swww matugen hyprlock kvantum kvantum-qt5
yay -S adw-gtk-theme ttf-jetbrains-mono-nerd
```
</details>

<details>
<summary><b>Terminal & Shell</b></summary>

```bash
sudo pacman -S kitty zsh tmux starship fastfetch eza bat
yay -S oh-my-zsh-git
```
</details>

<details>
<summary><b>Tools & Utils</b></summary>

```bash
sudo pacman -S neovim python python-pip ripgrep bc fzf gum thunar imv grim slurp wf-recorder wl-clipboard brightnessctl btop pacman-contrib
yay -S zed systemd-manager-tui wifitui bluetuith
```
</details>

<details>
<summary><b>Media</b></summary>

```bash
sudo pacman -S mpd mpc mpd-mpris playerctl wireplumber
yay -S rmpc wiremix zen-browser-bin
```
</details>

## Installation

### Quick Install

```bash
# 1. Backup your configs
cp -r ~/.config ~/.config.backup

# 2. Clone repository
git clone https://github.com/diominvd/vibegen-dots.git ~/.dotfiles
cd ~/.dotfiles

# 3. Install dependencies (see Dependencies section above)

# 4. Create required directories
mkdir -p ~/Pictures/Wallpapers ~/Videos/Screenrecords ~/Music

# 5. Remove conflicting configs
rm -rf ~/.config/{hypr,waybar,rofi,kitty,mako,fastfetch,nvim,tmux,zed,mpd}
rm -f ~/.zshrc

# 6. Deploy configs with stow
stow -v -t ~ fastfetch gtk-3.0 gtk-4.0 hypr kitty matugen mpd nvim rofi scripts tmux wallpapers waybar zed zen-browser zsh

# 7. Set zsh as default shell
chsh -s $(which zsh)

# 8. Reboot and select Hyprland session
```

### Post-Install

**Add wallpapers:**
```bash
cp your-wallpapers/* ~/Pictures/Wallpapers/
# Use Super + Shift + W to apply and generate color scheme
```

**Configure music:**
```bash
cp your-music/* ~/Music/
mpc update
```

## Keybinds

| Keybind | Action |
|---------|--------|
| `Super + Return` | Terminal |
| `Alt + Space` | System menu |
| `Super + Q` | Close window |
| `Super + M` | Exit Hyprland |
| `Super + L` | Lock screen |

See `~/.config/hypr/config/keybinds.conf` for full list.

## Troubleshooting

**Waybar not showing:**
```bash
killall waybar && waybar &
```

**Colors not applying:**
```bash
matugen image ~/Pictures/Wallpapers/your-wallpaper.jpg
hyprctl reload
```

**Check logs:**
```bash
journalctl -b | grep hyprland
```

## License

[MIT License](LICENSE)

---

<div align="center">

**If you like this config, give it a ⭐**

Made with ❤️ for the Hyprland community

</div>

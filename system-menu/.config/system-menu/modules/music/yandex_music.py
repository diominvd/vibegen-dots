import os
import subprocess
import time
from .utils import stop_music_logic

HOME = os.path.expanduser("~")
PY_PATH = f"{HOME}/.config/yamusic/venv/bin/python"
SCRIPT_PATH = f"{HOME}/.config/yamusic/yamusic_mpd.py"

def ensure_mpd_mpris():
    try:
        result = subprocess.run(
            ["pgrep", "-x", "mpd-mpris"],
            capture_output=True
        )
        
        if result.returncode != 0:
            subprocess.Popen(
                ["mpd-mpris"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(0.5)  # Give it time to initialize
    except Exception as e:
        print(f"Warning: Could not start mpd-mpris: {e}")

def launch_rmpc():
    try:
        result = subprocess.run(
            ["pgrep", "-f", "rmpc"],
            capture_output=True
        )
        
        if result.returncode != 0:
            subprocess.Popen(
                [
                    "kitty",
                    "--class", "music_player",
                    "--title", "music-player",
                    "-e", "rmpc"
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(0.3)  # Give window time to spawn
    except Exception as e:
        print(f"Warning: Could not launch rmpc: {e}")

def run_music():
    stop_music_logic()
    
    # Notify start
    subprocess.run(["notify-send", "Yandex Music", "Synchronizing library"])
    
    try:
        # Sync library
        subprocess.run(
            [PY_PATH, SCRIPT_PATH],
            input="1\n500\n",
            text=True,
            capture_output=True,
            check=True
        )
        
        subprocess.run(["mpc", "update", "--wait"], check=True, capture_output=True)
        ensure_mpd_mpris()
        subprocess.run(["mpc", "play"], check=True, capture_output=True)
        launch_rmpc()
        subprocess.run(["notify-send", "Yandex Music", "Playback started"])
        
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "Unknown error during sync"
        subprocess.run(["notify-send", "-u", "critical", "Yandex Music Error", error_msg])
        print(f"Process error: {e}")
        return False
    except FileNotFoundError:
        subprocess.run(["notify-send", "-u", "critical", "Yandex Music", "Script paths not found!"])
        return False
    except Exception as e:
        subprocess.run(["notify-send", "-u", "critical", "Yandex Music", f"Unexpected error: {str(e)}"])
        return False
    
    return True

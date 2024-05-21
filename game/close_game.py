import json
import sys
import time
from pathlib import Path

import pygame


def close_game(self):
    from audiomanager import AudioManager
    shutdown_sound = AudioManager(20, 0, 1, audio_file="music/shut-donw.mp3", play=True)
    with (Path(__file__).parent / "config.json").open("w") as config_file:
        json.dump(self.config_data, config_file)
    while shutdown_sound.get_busy():
        time.sleep(0.1)
    pygame.quit()
    sys.exit()
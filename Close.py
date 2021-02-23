import json
import sys
import pygame
from pathlib import Path
from Audio_Manager import Audio_Manager


class Close_Game:
    def __init__(self, config_data):
        shutdown_sound = Audio_Manager(20, 0, 1, audio_file="music/shut-donw.mp3",
                      play=True)
        with (Path(__file__).parent / "config.json").open("w") as config_file:
            json.dump(config_data, config_file)
        while shutdown_sound.get_busy():
            pass
        pygame.quit()
        sys.exit()
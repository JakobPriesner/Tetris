import json
from pathlib import Path
from threading import Thread

import pygame

from audiomanager import AudioManager
from close_game import close_game
from colormanager import ColorManager
from game import Game
from menus.options import Options
from menus.settings import Settings


class Menu:
    config_data = None
    audio = 0.2
    fps = 30
    clock = pygame.time.Clock()
    main_zoom = 0

    def __init__(self, _screen):
        self.screen = _screen
        self.main_zoom = _screen.get_width() * 0.08
        Menu.main_zoom = self.main_zoom
        with (Path(__file__).parent.parent / "config.json").open("rb") as config_file:
            self.config_data = json.load(config_file)

        self.audio_settings = self.config_data["Audio_Settings"]
        if not self.audio_settings["muted"]:
            self.background_musik = AudioManager(self.audio_settings["menu_background"], -1, 1, audio_file="music/menu.mp3",
                                                 play=True)
            self.effect_music = AudioManager(self.audio_settings["effects"], 0, 2, audio_file="music/level_up.mp3")
        else:
            self.background_musik = AudioManager(0, -1, 1, audio_file="music/menu.mp3", play=True)
            self.effect_music = AudioManager(0, 0, 2, audio_file="music/level_up.mp3")

        self.background_musik.play()
        self.color_manager = ColorManager(_screen, self.config_data["Color_Mode"])

        self.main_frame()

    def main_frame(self):
        done = False

        options = [Options(self.screen, "Play", (155, 300), self.color_manager),
                   Options(self.screen, "Settings", (123, 340), self.color_manager),
                   Options(self.screen, "Mute", (145, 380), self.color_manager),
                   Options(self.screen, "Exit", (159, 420), self.color_manager)]

        while not done:
            self.screen.fill(color=self.color_manager.MENU_COLOR)
            logo = pygame.image.load(Path(__file__).parent / "pictures" / "logo.png")
            self.screen.blit(logo, (50, 50))
            background_logo = pygame.image.load(Path(__file__).parent / "pictures" / "menu_background.png")
            self.screen.blit(background_logo, (0, 0))

            for option in options:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    option.hovered = True
                else:
                    option.hovered = False
                option.draw()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for option in options:
                        if option.rect.collidepoint(pygame.mouse.get_pos()):
                            if option.text == "Play":
                                self.effect_music.play("music/button_click.mp3")
                                Game(self.screen, self.color_manager, self.config_data, self)
                            elif option.text == "Settings":
                                self.effect_music.play("music/button_click.mp3")
                                settings = Settings(self.screen, None, self, self.config_data, self.background_musik, self.effect_music, self.color_manager, "menu", 100)
                                th = Thread(target=settings.main)
                                th.start()
                                return
                            elif option.text == "Mute":
                                self.effect_music.play("music/button_click.mp3")
                                self.background_musik.set_volume(0)
                                self.effect_music.set_volume(0)
                                self.config_data["Audio_Settings"]["muted"] = True
                                option.text = "Unmute"
                                option.pos = (122, 380)
                                option.set_rect()
                            elif option.text == "Unmute":
                                self.effect_music.play("music/button_click.mp3")
                                self.background_musik.set_volume(self.audio_settings["menu_background"])
                                self.effect_music.set_volume(self.audio_settings["effects"])
                                self.config_data["Audio_Settings"]["muted"] = False

                                option.text = "Mute"
                                option.pos = (145, 380)
                                option.set_rect()
                            elif option.text == "Exit":
                                self.effect_music.play("music/button_click.mp3")
                                done = True
                                close_game(self.config_data)
                if event.type == pygame.QUIT:
                    close_game(self.config_data)
            pygame.display.flip()
            self.clock.tick(self.fps)
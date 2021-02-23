from pathlib import Path
from Audio_Manager import Audio_Manager
from Game import game
from menus.Settings import Settings
from color_Manager import color_Manager
from menus.Option import Option
from Close import Close_Game
import pygame
import json


class menu:
    config_data = None
    audio = 0.2
    fps = 30
    clock = pygame.time.Clock()
    main_zoom = 0

    def __init__(self, _screen):
        self.screen = _screen
        with (Path(__file__).parent / "config.json").open("rb") as config_file:
            self.config_data = json.load(config_file)

        self.audio_settings = self.config_data["Audio_Settings"]
        if not self.audio_settings["muted"]:
            self.background_musik = Audio_Manager(self.audio_settings["menu_background"], -1, 1, audio_file="music/menu.mp3",
                                                  play=True)
            self.effect_music = Audio_Manager(self.audio_settings["effects"], 0, 2, audio_file="music/level_up.mp3")
        else:
            self.background_musik = Audio_Manager(0, -1, 1, audio_file="music/menu.mp3", play=True)
            self.effect_music = Audio_Manager(0, 0, 2, audio_file="music/level_up.mp3")

        self.background_musik.play()
        self.color_manager = color_Manager(_screen, self.config_data["Color_Mode"])
        self.color2 = color_Manager(_screen, self.config_data["Color_Mode"])

        self.game = game(self.screen, self.color_manager, self.config_data, self)

        self.main_frame()

    def main_frame(self):
        done = False

        options = [Option(self.screen, "Play", (155, 300), self.color_manager),
                   Option(self.screen, "Settings", (123, 340), self.color_manager),
                   Option(self.screen, "Mute", (145, 380), self.color_manager),
                   Option(self.screen, "Exit", (159, 420), self.color_manager)]

        while not done:
            self.screen.fill(color=self.color_manager.MENU_COLOR)
            logo = pygame.image.load("pictures/logo.png")
            self.screen.blit(logo, (50, 50))
            background_logo = pygame.image.load("pictures/menu_background.png")
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
                                self.game(self.screen, self.color_manager, self.config_data)
                            elif option.text == "Settings":
                                self.effect_music.play("music/button_click.mp3")
                                Settings(self.config_data, self.background_musik, self.effect_music, self.color_manager, "menu", 100, self.screen)
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
                                Close_Game(self.config_data)
                if event.type == pygame.QUIT:
                    Close_Game(self.config_data)
            pygame.display.flip()
            self.clock.tick(self.fps)
import pygame
import pygame_gui
from color_Manager import color_Manager
from menus.Option import Option
from Close import Close_Game
from menus.Slider import Slider


class Settings:
    def __init__(self, _screen, _game, _menu, config_data, backgorund_music, effect_music, color_manager, type, displacement, screen):
        self.type = type
        self.displacement = displacement
        self.config_data = config_data
        self.background_music = backgorund_music
        self.effect_music = effect_music
        self.color_manager = color_manager
        self.clock = pygame.time.Clock()
        self.effect_music.set_volume(self.config_data["Audio_Settings"]["effects"])
        self.screen = _screen
        self.game = _game
        self.menu = _menu

        self.main()

    def main(self):
        done = False
        options = [Option("Audio", (141, 220+self.displacement), self.color_manager),
                   Option("Colors", (137, 260+self.displacement), self.color_manager),
                   Option("Back", (151, 300+self.displacement), self.color_manager)]
        while not done:
            if self.config_data["Color_Mode"] == "NORMAL_MODE":
                background_image = pygame.image.load("pictures/normal_pause.png")
            else:
                background_image = pygame.image.load("pictures/dark_pause.png")
            self.screen.blit(background_image, ((380-background_image.get_width())/2, 175))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Close_Game(self.config_data)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for option in options:
                        if option.rect.collidepoint(pygame.mouse.get_pos()):
                            if option.text == "Audio":
                                self.effect_music.play("music/button_click.mp3")
                                self.audio()
                            elif option.text == "Colors":
                                self.effect_music.play("music/button_click.mp3")
                                done = True
                                self.color_settings()
                            elif option.text == "Back":
                                self.effect_music.play("music/button_click.mp3")
                                done = True
                                if type == "menu":
                                    self.menu(self.screen)
                                elif type == "game":
                                    self.game(self.color_manager, self.config_data)

            for option in options:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    option.hovered = True
                else:
                    option.hovered = False
                option.draw()

                text_font = pygame.font.SysFont('Calibri', 40, True, False)
                text = text_font.render("Settings", True, self.color_manager.HEADLINE)
                self.screen.blit(text, [123, 160+self.displacement])
            pygame.display.flip()


    def audio(self):
        if self.config_data["Color_Mode"] == "NORMAL_MODE":
            background_image = pygame.image.load("pictures/normal_pause.png")
        else:
            background_image = pygame.image.load("pictures/dark_pause.png")


        done = False
        manager = pygame_gui.UIManager((380, 650))
        heading_font = pygame.font.SysFont("Calibri", 40, True, False)
        heading_text = heading_font.render("Audio", True, self.color_manager.HEADLINE)

        menu_background_audio_value = Slider("Menu-Music: ", 80, 150 + self.displacement, color_Manager.DARKEST_GRAY, manager, self.config_data["Audio_Settings"]["menu_background"], (1, 100))
        game_backgorund_audio_value = Slider("Background-Music: ", 80, 210 + self.displacement, color_Manager.DARKEST_GRAY, manager, self.config_data["Audio_Settings"]["game_background"], (1, 100))
        effects_audio_value = Slider("Game-Effects: ", 80, 270 + self.displacement, color_Manager.DARKEST_GRAY, manager, self.config_data["Audio_Settings"]["effects"], (1, 100))
        if self.type == "menu":
            main_ref = menu_background_audio_value
        elif self.type == "game":
            main_ref = game_backgorund_audio_value
        else:
            main_ref = menu_background_audio_value

        if self.config_data["Audio_Settings"]["muted"]:
            text = "Unmute"
            position = (122, 330+self.displacement)
        else:
            text = "Mute"
            position = (145, 330+self.displacement)

        options = [Option(text, position, self.color_manager),
                   Option("Back", (145, 370+self.displacement), self.color_manager)]

        while not done:
            self.screen.blit(background_image, ((380-background_image.get_width())/2, 75+self.displacement))
            self.screen.blit(heading_text, (141, 110+self.displacement))
            time_delta = self.clock.tick(30)

            menu_background_audio_value.draw()
            game_backgorund_audio_value.draw()
            effects_audio_value.draw()

            if not self.config_data["Audio_Settings"]["muted"]:
                self.background_music.set_volume(main_ref.get_current_value())
                self.effect_music.set_volume(effects_audio_value.get_current_value())
            self.config_data["Audio_Settings"]["menu_background"] = menu_background_audio_value.get_current_value()
            self.config_data["Audio_Settings"]["game_background"] = game_backgorund_audio_value.get_current_value()
            self.config_data["Audio_Settings"]["effects"] = effects_audio_value.get_current_value()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Close_Game(self.config_data)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for option in options:
                        if option.rect.collidepoint(pygame.mouse.get_pos()):
                            if option.text == "Mute":
                                self.effect_music.play("music/button_click.mp3")
                                self.background_music.set_volume(0)
                                self.effect_music.set_volume(0)
                                self.config_data["Audio_Settings"]["muted"] = True
                                option.text = "Unmute"
                                option.pos = (122, 330+self.displacement)
                                option.set_rect()
                            elif option.text == "Unmute":
                                self.effect_music.play("music/button_click.mp3")
                                self.background_music.set_volume(self.config_data["Audio_Settings"]["menu_background"])
                                self.effect_music.set_volume(self.config_data["Audio_Settings"]["effects"])
                                self.config_data["Audio_Settings"]["muted"] = False
                                option.text = "Mute"
                                option.pos = (145, 330+self.displacement)
                                option.set_rect()
                            elif option.text == "Back":
                                done = True
                                self.main()
                manager.process_events(event)

            for option in options:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    option.hovered = True
                else:
                    option.hovered = False
                option.draw()

            if menu_background_audio_value.is_pressed():
                self.effect_music.play("music/button_click_down.mp3")
            if menu_background_audio_value.is_released():
                self.effect_music.play("music/button_click_up.mp3")
            if game_backgorund_audio_value.is_pressed():
                self.effect_music.play("music/button_click_down.mp3")
            if game_backgorund_audio_value.is_released():
                self.effect_music.play("music/button_click_up.mp3")
            if effects_audio_value.is_pressed():
                self.effect_music.play("music/button_click_down.mp3")
            if effects_audio_value.is_released():
                self.effect_music.play("music/button_click_up.mp3")


            manager.draw_ui(self.screen)
            manager.update(time_delta=time_delta)
            pygame.display.flip()
            self.clock.tick(30)

    def color_settings(self):
        heading_font = pygame.font.SysFont('Calibri', 40, True, False)
        heading_text = heading_font.render("Color Settings", True, self.color_manager.HEADLINE)
        options = [Option("Normal-Mode", (72, 200+self.displacement), self.color_manager),
                   Option("Dark-Mode", (96, 250+self.displacement), self.color_manager),
                   Option("BACK", (145, 290+self.displacement), self.color_manager)]

        if self.config_data["Color_Mode"] == "NORMAL_MODE":
            background_image = pygame.image.load("pictures/normal_pause.png")
        else:
            background_image = pygame.image.load("pictures/dark_pause.png")
        done = False
        while not done:
            self.screen.blit(background_image, ((380 - background_image.get_width()) / 2, 75+self.displacement))
            self.screen.blit(heading_text, (80, 110+self.displacement))
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
                            if option.text == "Normal-Mode":
                                self.effect_music.play("music/button_click.mp3")
                                self.color_manager.set_normalmode()
                                self.config_data['Color_Mode'] = "NORMAL_MODE"
                                self.color_settings()
                            elif option.text == "Dark-Mode":
                                self.effect_music.play("music/button_click.mp3")
                                self.color_manager.set_darkmode()
                                self.config_data['Color_Mode'] = "DARK_MODE"
                                self.color_settings()
                            elif option.text == "BACK":
                                self.effect_music.play("music/button_click.mp3")
                                done = True
                                self.main()
                if event.type == pygame.QUIT:
                    Close_Game(self.config_data)

            pygame.display.flip()
            self.clock.tick(30)
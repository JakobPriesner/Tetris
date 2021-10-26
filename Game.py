import pygame

from Audio_Manager import Audio_Manager
from Close import Close_Game
from Color_Manager import colors
from Tetris import Tetris
from menus.Loose_Menu import Loose_menu
from menus.Option import Option
from menus.Settings import Settings


class game:
    zoom = None

    def __init__(self, _screen, color_manager, config_data, _menu):
        self.audio_settings = config_data["Audio_Settings"]
        if not self.audio_settings["muted"]:
            self.background_musik = Audio_Manager(self.audio_settings["game_background"], -1, 1,
                                                  audio_file="music/game.mp3",
                                                  play=True)
            self.effect_music = Audio_Manager(self.audio_settings["effects"], 0, 2, audio_file="music/level_up.mp3")
        else:
            self.background_musik = Audio_Manager(0, -1, 1, audio_file="music/game.mp3", play=True)
            self.effect_music = Audio_Manager(0, 0, 2, audio_file="music/level_up.mp3")

        self.screen = _screen
        self.color_manager = color_manager
        self.done = False
        self.fps = 2
        self.clock = pygame.time.Clock()
        self.counter = 0
        self.zoom = int(_screen.get_width() * 0.08)
        self.game = Tetris(20, 10)
        self.config_data = config_data
        self.menu = _menu

        self.pressing_down = False
        self.pressing_left = False
        self.pressing_right = False
        self.loop()

    def loop(self):
        ticks = 0
        while not self.done:
            ticks += 1
            if ticks * self.fps >= 60:
                ticks = 0
                if self.game.state == "start":
                    self.game.go_down(self.effect_music)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Close_Game(self.config_data)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.game.rotate(self.effect_music)
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.pressing_down = True
                        self.fps += 14
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.pressing_left = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.pressing_right = True
                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.pressing_down = False
                        self.fps -= 14
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.pressing_left = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.pressing_right = False

                if self.pressing_down:
                    self.game.go_down(self.effect_music)
                if self.pressing_left:
                    self.game.left()
                if self.pressing_right:
                    self.game.right()

            self.screen.fill(color=self.color_manager.MENU_COLOR)
            for i in range(self.game.height):
                for j in range(self.game.width):
                    if self.game.field[i][j] == 0:
                        color = self.color_manager.LINE_COLOR
                        just_border = 1
                    else:
                        color = colors[self.game.field[i][j]]
                        just_border = 0
                    pygame.draw.rect(self.screen, color, [40 + j * self.zoom, 30 + i * self.zoom, self.zoom, self.zoom],
                                     just_border)
            # update the figures
            if self.game.Figure is not None:
                for i in range(4):
                    for j in range(4):
                        p = i * 4 + j
                        if p in self.game.Figure.image():
                            pygame.draw.rect(self.screen, self.game.Figure.color,
                                             [40 + (j + self.game.Figure.x) * self.zoom,
                                              30 + (i + self.game.Figure.y) * self.zoom, self.zoom, self.zoom])

            if ((self.game.score / 50) / self.game.level) > 1:
                self.effect_music.play("music/level_up.mp3")
                self.fps += 1
                self.game.level += 1
            if self.game.state == "gameover":
                Loose_menu(self.screen, self.game, self.color_manager, self.config_data)
                self.done = True
            # update the score and the level
            level_font = pygame.font.SysFont('Calibri', 25, True, False)
            text_level = level_font.render("Level " + str(self.game.level), True, self.color_manager.SCORE)
            self.screen.blit(text_level, [0, 0])

            score_font = pygame.font.SysFont('Calibri', 25, True, False)
            text_score = score_font.render("Score " + str(self.game.score), True, self.color_manager.SCORE)

            self.screen.blit(text_score, [text_score.get_width(), 0])

            pygame.display.flip()
            self.clock.tick(60)

        # call the Loose_menu
        Loose_menu(self.screen, self.game, self.color_manager, self.config_data)

    def pause_menu(self):
        old_game = self.game
        old_fps = self.fps
        screen = self.screen
        self.fps = 0
        self.color_manager.pale_frame(self.zoom, old_game, 7)
        done = False
        options = [Option(self.screen, "Resume", (123, 260), self.color_manager),
                   Option(self.screen, "Retry", (145, 300), self.color_manager),
                   Option(self.screen, "Settings", (123, 340), self.color_manager),
                   Option(self.screen, "Menu", (145, 380), self.color_manager),
                   Option(self.screen, "Exit", (159, 420), self.color_manager)]
        if self.config_data["Color_Mode"] == "NORMAL_MODE":
            background_image = pygame.image.load("pictures/normal_pause.png")
        else:
            background_image = pygame.image.load("pictures/dark_pause.png")

        while not done:
            screen.blit(background_image, ((380-background_image.get_width())/2, 125))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event == pygame.K_ESCAPE:
                        done = True
                        self.end_pause_menu(old_game, old_fps)
                if event.type == pygame.QUIT:
                    Close_Game(self.config_data)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for option in options:
                        if option.rect.collidepoint(pygame.mouse.get_pos()):
                            if option.text == "Resume":
                                self.effect_music.play("music/button_click.mp3")
                                done = True
                                self.end_pause_menu(old_game, old_fps)
                            elif option.text == "Retry":
                                self.effect_music.play("music/button_click.mp3")
                                game(self.screen, self.color_manager, self.config_data, self.menu)
                            elif option.text == "Settings":
                                Settings(self.screen, self.game, self.menu, self.config_data, self.background_musik, self.effect_music, self.color_manager, "game", -50, screen)
                            elif option.text == "Menu":
                                self.effect_music.play("music/button_click.mp3")
                                done = True
                                self.menu(screen)
                            elif option.text == "Exit":
                                self.effect_music.play("music/button_click.mp3")
                                Close_Game(self.config_data)
            for option in options:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    option.hovered = True
                else:
                    option.hovered = False
                option.draw()

                text_font = pygame.font.SysFont("Calibri", 40, True, False)
                text = text_font.render("PAUSE", True, self.color_manager.HEADLINE)
                screen.blit(text, [135, 160])
            pygame.display.flip()
            break

    def start_new_game(self):
        print("start new game")
        self.game = Tetris(20, 10)
        self.loop()

    def end_pause_menu(self, old_game, fps):
        self.fps = fps
        self.game = old_game
        self.color_manager.pale_frame(self.zoom, self.game, -7)
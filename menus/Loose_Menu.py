import pygame
from Audio_Manager import Audio_Manager
from Close import Close_Game


class Loose_menu:
    screen = None
    game = None
    zoom = None

    def __init__(self, _screen, _game, color_manager, config_data):
        self.color_manager = color_manager
        self.config_data = config_data
        self.screen = _screen
        self.game = _game
        self.zoom = 30
        self.color_manager.pale_frame(self.zoom, self.game, 7)

        self.audio_settings = self.config_data["Audio_Settings"]
        if not self.audio_settings["muted"]:
            self.background_musik = Audio_Manager(self.audio_settings["menu_background"], -1, 1,
                                                  audio_file="../music/menu.mp3",
                                                  play=True)
            self.effect_music = Audio_Manager(self.audio_settings["effects"], 0, 2, audio_file="../music/level_up.mp3")
        else:
            self.background_musik = Audio_Manager(0, -1, 1, audio_file="../music/menu.mp3", play=True)
            self.effect_music = Audio_Manager(0, 0, 2, audio_file="../music/level_up.mp3")

        self.loop()

    def loop(self):
        done = False
        clock = pygame.time.Clock()

        score_font = pygame.font.SysFont('Calibri', 40, True, False)
        if self.game.score > self.config_data['Highscore']:
            self.config_data['Highscore'] = self.game.score
            highscore_font = pygame.font.SysFont('Calibri', 70, True, False)
            text_congratulation = highscore_font.render("!!!NEW HIGHSCORE!!!: ", True, self.color_manager.HIGHSCORE)
            self.screen.blit(text_congratulation, [20, 300])
            text_score = score_font.render("Score: " + str(self.game.score), True, self.color_manager.HIGHSCORE)
            self.screen.blit(text_score, [100, 390])
        else:
            text_score = score_font.render("Level " + str(self.game.level), True, self.color_manager.HIGHSCORE)
            self.screen.blit(text_score, [127, 320])
            text_score = score_font.render("Score " + str(self.game.score), True, self.color_manager.HIGHSCORE)
            self.screen.blit(text_score, [100, 340])
            text_highscore = score_font.render("Highscore: " + str(self.config_data["Highscore"]), True,
                                               self.color_manager.SCORE)
            self.screen.blit(text_highscore, [100, 360])

        gameover_font = pygame.font.SysFont('Calibri', 70, True, False)
        text_gameover = gameover_font.render("Game Over!", True, self.color_manager.GAME_OVER)
        self.screen.blit(text_gameover, [15, 250])
        pygame.display.flip()

        pygame.mixer.music.load('music/failure.mp3')
        pygame.mixer.music.play(False, 0.5)
        while pygame.mixer.music.get_busy():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Close_Game(self.config_data)
                if event.type == pygame.K_ESCAPE:
                    self.game(self.color_manager, self.config_data)

        while not done:
            pygame.display.flip()
            clock.tick(2)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game(self.color_manager, self.config_data)
                        done = True
                if event.type == pygame.QUIT:
                    Close_Game(self.config_data)
import pygame
from Audio_Manager import Audio_Manager
from Close import Close_Game
from menus.Option import Option


class Loose_menu:
    screen = None
    game = None
    zoom = None

    def __init__(self, _screen, _game, color_manager, config_data):
        self.color_manager = color_manager
        self.config_data = config_data
        self.screen = _screen
        self.game = _game
        self.zoom = int(_screen.get_width() * 0.08)
        self.color_manager.pale_frame(self.zoom, self.game, 7)

        self.audio_settings = self.config_data["Audio_Settings"]
        if not self.audio_settings["muted"]:
            self.background_musik = Audio_Manager(self.audio_settings["menu_background"], -1, 1,
                                                  audio_file="./music/menu.mp3",
                                                  play=True)
            self.effect_music = Audio_Manager(self.audio_settings["effects"], 0, 2, audio_file="./music/level_up.mp3")
        else:
            self.background_musik = Audio_Manager(0, -1, 1, audio_file="./music/menu.mp3", play=True)
            self.effect_music = Audio_Manager(0, 0, 2, audio_file="./music/level_up.mp3")

        self.loop()

    def loop(self):
        done = False
        clock = pygame.time.Clock()

        score_font = pygame.font.SysFont('Calibri', 1*self.zoom, True, False)
        if self.game.score > self.config_data['Highscore']:
            self.config_data['Highscore'] = self.game.score
            highscore_font = pygame.font.SysFont('Calibri', 1*self.zoom, True, False)
            text_congratulation = highscore_font.render("!!!NEW HIGHSCORE!!!: ", True, self.color_manager.HIGHSCORE)
            self.screen.blit(text_congratulation, [self.get_width(text_congratulation), int(8.25*self.zoom)])
            text_score = score_font.render("Score: " + str(self.game.score), True, self.color_manager.HIGHSCORE)
            self.screen.blit(text_score, [self.get_width(text_score), int(12*self.zoom)])

        else:
            text_score = score_font.render("Level " + str(self.game.level), True, self.color_manager.HIGHSCORE)
            self.screen.blit(text_score, [self.get_width(text_score), int(10.2*self.zoom)])
            text_score = score_font.render("Score " + str(self.game.score), True, self.color_manager.HIGHSCORE)
            self.screen.blit(text_score, [self.get_width(text_score), int(11.4*self.zoom)])
            text_highscore = score_font.render("Highscore: " + str(self.config_data["Highscore"]), True,
                                               self.color_manager.SCORE)
            self.screen.blit(text_highscore, [self.get_width(text_highscore), int(7.8*self.zoom)])

        gameover_font = pygame.font.SysFont('Calibri', 2*self.zoom, True, False)
        text_gameover = gameover_font.render("Game Over!", True, self.color_manager.GAME_OVER)
        self.screen.blit(text_gameover, [self.get_width(text_gameover), int(6*self.zoom)])

        menu_font = pygame.font.SysFont('Calibri', 1*self.zoom, True, False)
        menu_text = menu_font.render("Retry", True, self.color_manager.HIGHSCORE)
        option = Option(self.screen, "Retry", (self.get_width(menu_text), int(13.2*self.zoom)), self.color_manager)

        pygame.display.flip()

        pygame.mixer.music.load('music/failure.mp3')
        pygame.mixer.music.play(False, 0.5)

        while not done:
            pygame.display.flip()
            clock.tick(2)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game(self.color_manager, self.config_data)
                        done = True
                    if option.rect.collidepoint(pygame.mouse.get_pos()):
                        self.effect_music.play("music/button_click.mp3")
                        self.game.start_new_game()
                if event.type == pygame.QUIT:
                    Close_Game(self.config_data)
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()

    def get_width(self, text):
        return (self.screen.get_width() - text.get_width()) / 2

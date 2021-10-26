import pygame

WHITE = (255, 255, 255)
DARK_WHITE = (190, 190, 190)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
HELLROT = (255, 10, 10)
GREEN = (0, 255, 0)
GRASSGREEN = (64, 255, 64)
MOODY_GREEN = (49, 23, 131)
HELLBLAU = (128, 255, 128)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
BRIGHT_GRAY = (150, 150, 150)
DARK_GRAY = (64, 64, 64)
DARKEST_GRAY = (25, 25, 25)

colors = [
    (0, 0, 0),
    (0, 240, 240),  # vier in einer reihe
    (0, 0, 240),  # reversed l
    (240, 0, 160),  # l
    (240, 240, 0),  # Block
    (0, 240, 0),  # s
    (160, 0, 240),  # t
    (240, 0, 0),  # reversed s

    # darker_colors
    (0, 160, 160),  # vier in einer reihe
    (0, 0, 160),  # reversed l
    (160, 0, 80),  # l
    (160, 160, 0),  # Block
    (0, 160, 0),  # s
    (80, 0, 160),  # t
    (160, 0, 0)  # reversed s
]


class Color_Manager:
    Color_Mode = "NORMAL_MODE"
    MENU_COLOR = WHITE
    LINE_COLOR = GRAY
    BUTTON_COLOR = BLUE
    HOVERED_BC = BLACK
    GAME_OVER = RED
    SCORE = GRAY
    HIGHSCORE = RED
    HEADLINE = BLUE

    def __init__(self, _screen, color_Mode):
        if color_Mode == "NORMAL_MODE":
            self.set_normalmode()
        else:
            self.set_darkmode()
        self.screen = _screen

    def set_darkmode(self):
        self.MENU_COLOR = DARK_GRAY
        self.LINE_COLOR = DARK_WHITE
        self.BUTTON_COLOR = GREEN
        self.HOVERED_BC = WHITE
        self.GAME_OVER = HELLROT
        self.SCORE = GREEN
        self.HIGHSCORE = GREEN
        self.Color_Mode = "DARK_MODE"

    def set_normalmode(self):
        self.MENU_COLOR = WHITE
        self.LINE_COLOR = GRAY
        self.BUTTON_COLOR = BLUE
        self.HOVERED_BC = BLACK
        self.GAME_OVER = RED
        self.SCORE = GRAY
        self.HIGHSCORE = RED
        self.Color_Mode = "NORMAL_MODE"

    def pale_frame(self, zoom, game, changing_value):
        # Prepare game-field for loose-menu
        if self.Color_Mode == "NORMAL_MODE":
            color = GRAY
            line_color = DARKEST_GRAY
        else:
            color = DARKEST_GRAY
            line_color = DARK_GRAY
        self.screen.fill(color=color)

        for i in range(game.height):
            for j in range(game.width):
                if game.field[i][j] == 0 and self.Color_Mode == "DARK_MODE":
                    pygame.draw.rect(self.screen, line_color,
                                     [40 + j * zoom, 30 + i * zoom, zoom, zoom],
                                     1)
        # update the figures
        for figure in game.figures:
            if figure is not None:
                for i in range(4):
                    for j in range(4):
                        p = i * 4 + j
                        if p in figure.image():
                            pygame.draw.rect(self.screen, colors[figure.type + 1 + changing_value],
                                             [35 + (j + figure.x) * zoom,
                                              30 + (i + figure.y) * zoom, zoom, zoom])
        pygame.display.flip()

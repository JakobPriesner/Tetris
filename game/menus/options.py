import pygame


class Options:
    hovered = False

    def __init__(self, _screen, text, pos, color_mode):
        self.screen = _screen
        self.text = text
        self.pos = pos
        self.color_manager = color_mode
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        self.screen.blit(self.rend, self.rect)

    def set_rend(self):
        menu_font = pygame.font.SysFont('Calibri', 40, True, False)
        # menu_font = pygame.font.Font("fonts/pixel.TTF", 40)
        self.rend = menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return self.color_manager.HOVERED_BC
        else:
            return self.color_manager.BUTTON_COLOR

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos
from color_Manager import color_Manager
from Menu import menu
import pygame


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((380, 650))
    pygame.display.set_icon(pygame.image.load("tetris.png"))
    pygame.display.set_caption("Tetris by Jakob Priesner")
    color_manager = color_Manager
    menu(screen)

pygame.quit()

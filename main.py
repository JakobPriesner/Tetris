from Menu import menu
import pygame


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((570, 975))
    pygame.display.set_icon(pygame.image.load("pictures/tetris.png"))
    pygame.display.set_caption("Tetris by Jakob Priesner")
    menu(screen)

pygame.quit()

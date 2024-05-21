from pathlib import Path

import pygame

from menu import Menu

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((570, 975))
    pygame.display.set_icon(pygame.image.load(Path(__file__).parent / "pictures" / "tetris.png"))
    pygame.display.set_caption("Tetris by Jakob Priesner")
    Menu(screen)

pygame.quit()

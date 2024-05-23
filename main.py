import pygame
from pygame import Surface
from pygame.locals import *
import sys

from src.game_state import GameState

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)
win.fill(WHITE)
pygame.display.set_caption("Wizard101 Showdown")

clientNumber = 0

class CardWindow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/scarab.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, surface: Surface):
        surface.blit(self.image, self.rect)

    def setImage(self, image: str):
        self.image = pygame.image.load(image)

def main():




    run = True
    while run:
        center = (win.get_width() // 2, win.get_height() // 2)
        hand = [
            CardWindow(center[0]-450, center[1]+200),
            CardWindow(center[0]-300, center[1]+200),
            CardWindow(center[0]-150, center[1]+200),
            CardWindow(center[0], center[1]+200),
            CardWindow(center[0]+150, center[1]+200),
            CardWindow(center[0]+300, center[1]+200),
            CardWindow(center[0]+450, center[1]+200),
        ]
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    run = False
                    pygame.quit()

        win.fill(WHITE)
        for card in hand:
            card.draw(win)

        pygame.display.update()
        FramePerSec.tick(FPS)
            


            


    

if __name__ == "__main__":
    main()
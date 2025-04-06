import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1200, 800))
screen.fill((0, 35, 30))
player = pygame.rect.Rect(580, 380, 40, 40)
pygame.draw.rect(screen, (225, 0, 0), player)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
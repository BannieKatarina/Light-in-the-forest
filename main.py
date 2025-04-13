import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1200, 800))
player = pygame.rect.Rect(580, 380, 40, 40)
clock = pygame.time.Clock()
actons = {pygame.K_w: [1, -1], pygame.K_s: [1, 1], pygame.K_a: [0, -1], pygame.K_d: [0, 1]}
motion = [0, 0]
speed = 5

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            motion[actons[event.key][0]] += actons[event.key][1]
        if event.type == pygame.KEYUP:
            motion[actons[event.key][0]] -= actons[event.key][1]
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0, 35, 30))
    player = player.move(motion[0] * speed, motion[1] * speed)
    pygame.draw.rect(screen, (225, 0, 0), player)
    pygame.display.update()
    clock.tick(60)
import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1200, 800))
player = pygame.rect.Rect(580, 380, 40, 40)
clock = pygame.time.Clock()
motion = [0, 0]
speed = 5

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                motion[1] -= 1
            if event.key == pygame.K_s:
                motion[1] += 1
            if event.key == pygame.K_a:
                motion[0] -= 1
            if event.key == pygame.K_d:
                motion[0] += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                motion[1] += 1
            if event.key == pygame.K_s:
                motion[1] -= 1
            if event.key == pygame.K_a:
                motion[0] += 1
            if event.key == pygame.K_d:
                motion[0] -= 1
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0, 35, 30))
    player = player.move(motion[0] * speed, motion[1] * speed)
    pygame.draw.rect(screen, (225, 0, 0), player)
    pygame.display.update()
    clock.tick(60)
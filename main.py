import pygame
import sys

class Player():
    def __init__(self, x, y):
        self.player = pygame.rect.Rect(x, y, 100, 100)
        self.speed = 8
    def update(self):
        pygame.draw.rect(screen, (255, 0, 0), self.player)
    def move(self, motion):
        self.player = self.player.move(motion[0] * self.speed, motion[1] * self.speed)

pygame.init()

screen = pygame.display.set_mode((1200, 800))
player = Player(550, 350)
clock = pygame.time.Clock()
actons = {pygame.K_w: [1, -1], pygame.K_s: [1, 1], pygame.K_a: [0, -1], pygame.K_d: [0, 1]}
motion = [0, 0]
speed = 5

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key in actons:
            motion[actons[event.key][0]] += actons[event.key][1]
        if event.type == pygame.KEYUP and event.key in actons:
            motion[actons[event.key][0]] -= actons[event.key][1]
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0, 35, 30))
    player.move(motion)
    player.update()
    pygame.display.update()
    clock.tick(60)
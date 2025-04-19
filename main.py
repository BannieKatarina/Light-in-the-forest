import pygame
import sys


class Player():
    def __init__(self, x, y):
        self.player = pygame.rect.Rect(x, y, 100, 100)
        self.speed = 8

    def update(self):
        pygame.draw.rect(screen, (255, 0, 0), self.player)

    def collision(self, news, object):
        res = ["not", "not"]
        y1, x1 = self.player.y, self.player.x
        y2, x2 = y1 + self.player.height, x1 + self.player.width
        if not (y2 <= object.obj.y or y1 >= object.obj.y + object.obj.height):
            if object.obj.x <= news[0] <= object.obj.x + object.obj.width:
                res[0] = "left"
            elif object.obj.x <= news[2] <= object.obj.x + object.obj.width:
                res[0] = "right"
        if not (x1 >= object.obj.x + object.obj.width or x2 <= object.obj.x):
            if object.obj.y <= news[1] <= object.obj.y + object.obj.height:
                res[1] = "down"
            elif object.obj.y <= news[3] <= object.obj.y + object.obj.height:
                res[1] = "up"
        return res
    
    def move(self, motion, objects):
        x1, y1 = self.player.x, self.player.y
        x2, y2 = self.player.x + self.player.height, self.player.y + self.player.width
        new_x1, new_x2 = x1 + motion[0] * self.speed, x2 + motion[0] * self.speed
        new_y1, new_y2 = y1 + motion[1] * self.speed, y2 + motion[1] * self.speed
        for obj in objects:
            if not obj.passive:
                res = self.collision([new_x1, new_y1, new_x2, new_y2], obj)
                if res[0] == "left":
                    new_x1 = obj.obj.x + obj.obj.width + 1
                    new_x2 = new_x1 + 100
                elif res[0] == "right":
                    new_x2 = obj.obj.x
                    new_x1 = new_x2 - 100
                if res[1] == "down":
                    new_y1 = obj.obj.y + obj.obj.height + 1
                    new_y2 = new_y1 + 100
                elif res[1] == "up":
                    new_y2 = obj.obj.y
                    new_y1 = new_y2 - 100
        self.player = pygame.rect.Rect(new_x1, new_y1, 100, 100)
                

class Object():
    def __init__(self, color, x, y, width, height, passive=True):
        self.obj = pygame.rect.Rect(x, y, width, height)
        self.color = color
        self.passive = passive
        
    def update(self):
        pygame.draw.rect(screen, self.color, self.obj)
        

pygame.init()

screen = pygame.display.set_mode((1200, 800))
player = Player(550, 350)
start = Object((0, 255, 0), 400, 200, 400, 400)
wall1 = Object((0, 0, 255), 100, 30, 20, 400, False)
wall2 = Object((0, 0, 255), 0, 250, 200, 30, False)
objects = [start, wall1, wall2]
clock = pygame.time.Clock()
actons = {pygame.K_w: [1, -1], pygame.K_s: [1, 1], pygame.K_a: [0, -1], pygame.K_d: [0, 1]}
motion = [0, 0]

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
    player.move(motion, objects)
    for obj in objects:
        obj.update()
    player.update()
    pygame.display.update()
    clock.tick(60)
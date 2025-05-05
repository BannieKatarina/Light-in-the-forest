import pygame
import sys
from classes import Player, Camera, Object, Wall, Item, Interface, Branch
# import random

pygame.init()

screen = pygame.display.set_mode((1200, 800))
player = Player(screen, 550, 350)
start = Object(screen, (0,  255, 0), 400, 200, 400, 400)
wall1 = Wall(screen, (0, 0, 255), 100, 30, 20, 400)
wall2 = Wall(screen, (0, 0, 255), 0, 250, 200, 30)
objects = [start, wall1, wall2]
items = [Item(screen, (0, 255, 255), 1000, 150), Branch(screen, 750, 570)]
# items = [Item(screen, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), random.randint(0, 1100), random.randint(0, 700), "1") for q in range(random.randint(5, 7))]
cam = Camera(player, objects + items)
health = Interface(screen, player)
clock = pygame.time.Clock()
actons = {pygame.K_w: [1, -1], pygame.K_s: [1, 1], pygame.K_UP: [1, -1], pygame.K_DOWN: [1, 1],
          pygame.K_a: [0, -1], pygame.K_d: [0, 1], pygame.K_LEFT: [0, -1], pygame.K_RIGHT: [0, 1]}
motion = [0, 0]
f = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key in actons:
            motion[actons[event.key][0]] += actons[event.key][1]
        if event.type == pygame.KEYUP and event.key in actons:
            motion[actons[event.key][0]] -= actons[event.key][1]
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            health.use_branch()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            f = not f
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            new_items = []
            for i in range(len(items)):
                if items[i].pick_up and len(player.inventory) < 5:
                    player.collect_item(items[i])
                else:
                    new_items.append(items[i])
            items = new_items
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if health.leight <= 0:
        pygame.quit()
        sys.exit()
    screen.fill((0, 35, 30))
    cam.move_objects(motion)
    cam.update(objects + items)
    for itm in items:
        itm.check_pick_up(player)
    player.update()
    if f:
        player.show_inventory()
    health.update()
    pygame.display.update()
    clock.tick(60)
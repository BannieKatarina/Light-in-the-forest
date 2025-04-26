import pygame

class Player():
    def __init__(self, screen, x, y):
        self.player = pygame.rect.Rect(x, y, 100, 100)
        self.x1, self.y1 = x, y
        self.x2, self.y2 = x + 100, y + 100
        self.screen = screen
        self.speed = 8
        self.inventory = []
    
    def show_inventory(self):
        inv = pygame.rect.Rect(395, 700, 410, 90)
        pygame.draw.rect(self.screen, (255, 255, 0), inv)
        block = pygame.rect.Rect(405, 710, 70, 70)
        for x in range(5):
            pygame.draw.rect(self.screen, (0, 0, 0), block)
            if x < len(self.inventory):
                pygame.draw.circle(self.screen, self.inventory[x].color, block.center, 17.5)
            block = block.move(80, 0)

    def collision(self, news, object): # с какой стороны объекта пересекаем
        res = ["not", "not"]
        if not (self.y2 <= object.obj.y or self.y1 >= object.obj.y + object.obj.height):
            if object.obj.x <= news[0] <= object.obj.x + object.obj.width:
                res[0] = "right"
            elif object.obj.x <= news[2] <= object.obj.x + object.obj.width:
                res[0] = "left"
        if not (self.x1 >= object.obj.x + object.obj.width or self.x2 <= object.obj.x):
            if object.obj.y <= news[1] <= object.obj.y + object.obj.height:
                res[1] = "down"
            elif object.obj.y <= news[3] <= object.obj.y + object.obj.height:
                res[1] = "up"
        return res
    
    def collect_item(self, item):
        self.inventory += [item]
    
    def update(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.player)


class Camera():
    def __init__(self, player, objects):
        self.pl = player
        self.objs = objects
    
    def move_objects(self, motion):
        impossible_move = set()
        l, r, d, u = self.pl.speed + 2, self.pl.speed + 2, self.pl.speed + 2, self.pl.speed + 2
        action = [-motion[0] * self.pl.speed, -motion[1] * self.pl.speed]
        new_x1, new_y1 = self.pl.x1 + motion[0] * self.pl.speed, self.pl.y1 + motion[1] * self.pl.speed
        new_x2, new_y2 = new_x1 + self.pl.player.w, new_y1 + self.pl.player.h
        for obj in self.objs:
            if obj.type == "Wall":
                ways = self.pl.collision([new_x1, new_y1, new_x2, new_y2], obj)
                if ways[0] == "left":
                    l = min(l, new_x2 - obj.obj.x)
                elif ways[0] == "right":
                    r = min(r, obj.obj.x + obj.obj.w - new_x1)
                if ways[1] == "down":
                    d = min(d, obj.obj.y + obj.obj.h - new_y1)
                elif ways[1] == "up":
                    u = min(u, new_y2 - obj.obj.y)
                impossible_move.add(ways[0])
                impossible_move.add(ways[1])
        if "left" in impossible_move:
            action[0] += l
        elif "right" in impossible_move:
            action[0] -= r
        if "down" in impossible_move:
            action[1] -= d
        elif "up" in impossible_move:
            action[1] += u
        for obj in self.objs:
            obj.move(action)
            
    
    def update(self, objs):
        self.objs = objs
        for el in self.objs:
            el.update()


class Object():
    def __init__(self, screen, color, x, y, width, height):
        self.obj = pygame.rect.Rect(x, y, width, height)
        self.color = color
        self.screen = screen
        self.type = "Object"
    
    def move(self, motion):
        self.obj = pygame.rect.Rect(self.obj.x + motion[0], self.obj.y + motion[1], self.obj.w, self.obj.h)

    def move_partly(self, ways):
        l, r, d, u = ways
        dif1, dif2 = r - l, d - u
        self.obj = pygame.rect.Rect(self.obj.x + dif1, self.obj.y + dif2, self.obj.w, self.obj.h)

    def update(self):
        pygame.draw.rect(self.screen, self.color, self.obj)

class Wall(Object):
    def __init__(self, screen, color, x, y, width, height):
        super().__init__(screen, color, x, y, width, height)
        self.type = "Wall"

class Item(Object):
    def __init__(self, screen, color, x, y, info):
        super().__init__(screen, color, x, y, 100, 100)
        self.type = "Item"
        self.info = info
    
    def update(self):
        pygame.draw.circle(self.screen, self.color, self.obj.center, 5)
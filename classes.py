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

    def collision(self, news, object):
        res = ["not", "not"]
        if not (self.y2 <= object.obj.y or self.y1 >= object.obj.y + object.obj.height):
            if object.obj.x <= news[0] <= object.obj.x + object.obj.width:
                res[0] = "left"
            elif object.obj.x <= news[2] <= object.obj.x + object.obj.width:
                res[0] = "right"
        if not (self.x1 >= object.obj.x + object.obj.width or self.x2 <= object.obj.x):
            if object.obj.y <= news[1] <= object.obj.y + object.obj.height:
                res[1] = "down"
            elif object.obj.y <= news[3] <= object.obj.y + object.obj.height:
                res[1] = "up"
        return res
    
    def collect_item(self, item):
        self.inventory += [item]
    
    def move(self, motion, objects):
        new_x1, new_x2 = self.x1 + motion[0] * self.speed, self.x2 + motion[0] * self.speed
        new_y1, new_y2 = self.y1 + motion[1] * self.speed, self.y2 + motion[1] * self.speed
        for obj in objects:
            if obj.type == "Wall":
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
        self.x1, self.y1 = new_x1, new_y1
        self.x2, self.y2 = new_x1 + 100, new_y1 + 100

    def update(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.player)
                

class Object():
    def __init__(self, screen, color, x, y, width, height):
        self.obj = pygame.rect.Rect(x, y, width, height)
        self.color = color
        self.screen = screen
        self.type = "Object"

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
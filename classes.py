import pygame

class Player():
    def __init__(self, screen, x, y):
        self.player = pygame.rect.Rect(x, y, 20, 20)
        self.x1, self.y1 = x, y
        self.x2, self.y2 = x + 20, y + 20
        self.screen = screen
        self.speed = 8
        self.branches = 0
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
        if item.type == "Branch":
            self.branches += 1
        else:
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

    def update(self):
        pygame.draw.rect(self.screen, self.color, self.obj)

class Wall(Object):
    def __init__(self, screen, color, x, y, width, height):
        super().__init__(screen, color, x, y, width, height)
        self.type = "Wall"

class Item(Object):
    def __init__(self, screen, color, x, y):
        super().__init__(screen, color, x, y, 100, 100)
        self.type = "Item"
        self.pick_up = False
    
    def check_pick_up(self, pl):
        if pl.collision([pl.x1, pl.y1, pl.x2, pl.y2], self) != ["not", "not"]:
            self.pick_up = True
        else:
            self.pick_up = False
    
    def update(self):
        if self.pick_up:
            pygame.draw.circle(self.screen, (255, 0, 0), self.obj.center, 8)    
        pygame.draw.circle(self.screen, self.color, self.obj.center, 5)

class Branch(Item):
    def __init__(self, screen, x, y):
        super().__init__(screen, (139, 69, 19), x, y)
        self.type = "Branch"

class Interface():
    def __init__(self, screen, player):
        self.screen = screen
        self.pl = player
        self.leight = 100
        self.cnt = 0
        self.branch_box = pygame.rect.Rect(7, 50, 40, 40)
        self.box = pygame.rect.Rect(7, 7, self.leight * 2.5 + 6, 37)
        self.bar = pygame.rect.Rect(10, 10, self.leight * 2.5, 30)

    def update(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.branch_box, 3)
        pygame.draw.circle(self.screen, (139, 69, 19), self.branch_box.center, 7)
        font = pygame.font.SysFont("Comic Sans", 14)
        text = font.render(str(self.pl.branches), 0, (255, 255, 255))
        self.screen.blit(text, [34, 68])
        self.cnt += 1
        if self.cnt % 120 == 0:
            self.leight -= 5
            self.bar = pygame.rect.Rect(10, 10, self.leight * 2.5, 30)
            self.cnt = 0
        pygame.draw.rect(self.screen, (255, 0, 0), self.box)
        pygame.draw.rect(self.screen, (255, 184, 65), self.bar)
    
    def use_branch(self):
        if self.pl.branches:
            self.leight = min(105, self.leight + 25)
            self.pl.branches -= 1
            self.update()
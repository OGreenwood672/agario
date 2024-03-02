import pygame
import random
from math import pi

WIDTH = 500
HEIGHT = 500

rangeSmall = (2, 4)
rangePlayer = (6, 8)

class Blob:
    def __init__(self, x, y, r, identity): # creates blob object
        self.x = x
        self.y = y
        self.r = r
        self.identity = identity
        colours = [(0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255),
        (192,192,192), (128,128,128), (128,0,0), (128,128,0), (0,128,0), (128,0,128), (0,128,128), (0,0,128)]
        self.colour = random.choice(colours)
    
    def draw(self, DISPLAY): # draws blob
        pygame.draw.circle(DISPLAY, self.colour, (int(self.x), int(self.y)), int(self.r))
    
    def dist(self, other): # works out distance between self and other
        return int(((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5)

    def moveCorpse(self, players): # moves dead blob to an area where there is no other blobs
        if isinstance(self, Player):
            self.r = random.randrange(*rangePlayer)
        else:
            self.r = random.randrange(*rangeSmall)
        badPlacement = True
        while badPlacement:
            self.x = random.randint(WIDTH * 0.1, WIDTH * 0.9)
            self.y = random.randint(HEIGHT * 0.1, HEIGHT * 0.9)
            for player in players:
                if self.dist(player) < self.r + player.r and player != self:
                    break
            else:
                badPlacement = False

class Player(Blob):
    def __init__(self, x, y, r, identity, players): # creates player object
        super().__init__(x, y, r, identity)
        self.maxSpeed = 5
        self.score = 0
        self.name = self.getNames(players)
    
    def consume(self, other): # consumes a fraction of the other's mass
        intrest = 0.2 if self.r < 30 else 0.01
        totalMass = pi * self.r ** 2 + (pi * other.r ** 2) * intrest
        self.r = (totalMass / pi) ** 0.5
    
    def updateScore(self):
        self.score = int(self.r * 100)

    def getNames(self, players): # gets name from names.txt; each name is only used once
        taken = [player.name for player in players]
        names = []
        with open('names.txt', 'r') as f:
            for name in f:
                names.append(name[:-1])
        name = random.choice(names)
        while name in taken:
            name = random.choice(names)
        return name
            

    def move(self, width, height): # moves the player using mouse coords
        if pygame.mouse.get_focused(): # returns 0 when mouse is not on screen
            pos = pygame.mouse.get_pos()

            vel = (1 / self.r) # speed relates to size

            abs_change = pos[0] - width / 2 # centers x axis so 0 becomes -(width/2)
            if abs_change > 0:
                change = min(abs_change, self.maxSpeed)
            else:
                change = max(abs_change, -self.maxSpeed)

            new_x = change * vel
            if int(self.x + new_x) in range(int(WIDTH * 0.1), int(WIDTH * 0.9)):
                self.x += new_x

            abs_change = pos[1] - height / 2 # centers y axis so 0 becomes -(height/2)
            if abs_change > 0:
                change = min(abs_change, self.maxSpeed)
            else:
                change = max(abs_change, -self.maxSpeed)

            new_y = change * vel # moves it a fraction of the amount
            if int(self.y + new_y) in range(int(HEIGHT * 0.1), int(HEIGHT * 0.9)):
                self.y += new_y

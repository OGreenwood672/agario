import pygame

pygame.font.init()

class Scoreboard:
    def __init__(self, DISPLAY, width, height, player): # initilizes scoreboard object
        self.player = player
        self.DISPLAY = DISPLAY
        self.width = width
        self.height = height
        self.colours = {'black': (0, 0, 0), 'white':(255, 255, 255), 'grey': (120, 121, 128)}

    def renderText(self, text: str, size: int, x: int, y: int, colour: tuple): # allows text to be rendered
        font = pygame.font.SysFont(None, size)
        text = font.render(text, True, colour)
        self.DISPLAY.blit(text, (int(x), int(y)))
    
    def showNames(self, players): # shows all players names
        for player in players:
            self.renderText(player.name, int(self.width * 0.03), int(player.x - player.r), int(player.y + player.r), self.colours['black'])
    
    def sortPlayers(self, players): # sorts data to show top 3 + player
        players = sorted(players, key=lambda x: -x.score)
        players = [(index + 1, player.name, player.score) for index, player in enumerate(players) if (index <= 3 or player == self.player)]
        return players
    
    def showScore(self): # shows player's mass
        pygame.draw.rect(self.DISPLAY, self.colours['grey'], [int(self.width * 0.04), int(self.height * 0.02), int(self.width * 0.2), int(self.height * 0.05)])
        self.renderText('Mass: '+str(self.player.score), int(self.width * 0.05), int(self.width * 0.05), int(self.height * 0.03), self.colours['black'])
    
    def showLeaderboard(self, data): # creates a leaderboard
        lbHeight = int(len(data) * self.height * 0.05)
        pygame.draw.rect(self.DISPLAY, self.colours['grey'], [int(self.width * 0.7), int(self.height * 0.04), int(self.width * 0.28), lbHeight])
        y = self.height * 0.05
        delta_y = self.height * 0.05
        for info in data:
            self.renderText(str(info[0]) + '.', int(self.width * 0.05), int(self.width * 0.72), int(y), self.colours['black'])
            self.renderText(str(info[1]), int(self.width * 0.05), int(self.width * 0.75), int(y), self.colours['black'])
            self.renderText(str(info[2]), int(self.width * 0.05), int(self.width * 0.9), int(y), self.colours['black'])
            y += delta_y 

    def show(self, players): # shows the leaderboard and player's mass
        self.showScore()
        self.showLeaderboard(self.sortPlayers(players))
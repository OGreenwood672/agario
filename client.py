import pygame

from network import Network
from blobObject import Player
from scoreboard import Scoreboard

WIDTH = 500
HEIGHT = 500

DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")

def draw(s, background, player, players, blobs): # Draws zoomed in version of screen

    allBlobs = [*players, *blobs]

    main = DISPLAY.copy() # creates copy of Display as normal surfaces are locked
    s.DISPLAY = main # Allows the info to be displayed on zoomed version

    main.blit(background, (0, 0)) # shows background

    for blob in allBlobs: # draws blobs like normal
        blob.draw(main)
    
    s.showNames(players) # shows players names

    DISPLAY.blit(main, (0, 0)) # displays copy of screen on screen

    rect = pygame.Rect(0, 0, int(player.r * 10), int(player.r * 10)) # gets rect size
    rect.center = (int(player.x), int(player.y)) # centers the rect around the client

    rect.clamp_ip(main.get_rect()) # make sure the rect doesn't go off screen

    sub = main.subsurface(rect) # copy the area of the rect to a subsurface

    sub = pygame.transform.scale(sub, (WIDTH, HEIGHT)) # scales the subsurface to screen size
    DISPLAY.blit(sub, (0, 0)) # displays

    s.DISPLAY = DISPLAY # changes scoreboards normal surface back to normal display



def main():
    run = True
    n = Network() # functions which allow data to be sent to server
    player = n.player # Recieve player object from server
    clock = pygame.time.Clock()

    bg = pygame.image.load('agarBG.png') # loads and scales background
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    while run:

        players, blobs = n.send(player) # recieves data
        player = [x for x in players if x.identity == player.identity][0] # updates client's player object

        for event in pygame.event.get(): # checks if client has quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        s = Scoreboard(DISPLAY, WIDTH, HEIGHT, player) # creates a scoreboard object

        player.move(WIDTH, HEIGHT) # chekcs if player has moved
        draw(s, bg, player, players, blobs)# draws screen
        player.updateScore() # updates players score

        s.show(players) # shows a scoreboard and player's mass

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
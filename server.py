import socket
from _thread import *
import pickle
import random
import pygame
import time

from blobObject import Blob, Player
from scoreboard import Scoreboard


server = socket.gethostbyname(socket.gethostname()) # gets ip address
port = 6720 # port number

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # set up server
s.bind((server, port))
s.listen()
print('[RUNNING] server starting...') # server message

WIDTH = 500 # Global Variables
HEIGHT = 500
rangePlayer = (6, 8)
rangeSmall = (2, 4)

blobs = [] # small edible blobs
players = [] # players

def addBlobs(num): # creates the number of specified edible blobs then returns next ID
    for numID in range(num):
        blobs.append(Blob(random.randint(WIDTH * 0.1, WIDTH * 0.9), random.randint(HEIGHT * 0.1, HEIGHT * 0.9), random.randrange(*rangeSmall), numID))
    return numID

def collision(player, blobs): # checks if a player has eaten a small edible blob, if so the blob is consumed and moved elsewhere
    for blob in blobs:
        if player.dist(blob) < player.r + blob.r:
            player.consume(blob)
            blob.moveCorpse([*players, *blobs])

def playerColission(players, blobs): # Checks if player had been eaten by a player, if so is smaller player is consumed and moved
    for player in players:
        for player2 in players:
            if player.dist(player2) < player.r + player2.r and not (player is player2) and player.r > player2.r:
                player.consume(player2)
                player2.moveCorpse([*players, *blobs])

def newPlayer(conn, playerID): # main loop on server side for client

    #creates the client and sends it's player object to main loop
    currentPlayer = Player(random.randrange(WIDTH * 0.1, WIDTH * 0.9), random.randrange(HEIGHT * 0.1, HEIGHT * 0.9), random.randrange(*rangePlayer), playerID, players)
    players.append(currentPlayer)
    conn.send(pickle.dumps(currentPlayer))

    while True:
        try:
            currentPlayer = pickle.loads(conn.recv(2048)) # gets edited player object; eg different x
            players[players.index([player for player in players if player.identity == currentPlayer.identity][0])] = currentPlayer # changes the global occurence of that player

            collision(currentPlayer, blobs) # checks if player has eaten small edible blob
            playerColission(players, blobs)# checks if a player has been consumed
            conn.sendall(pickle.dumps((players, blobs))) # sends data to client
            
        except: # if left ga,e
            break

    print('[DISCONNECTED!]') # player had disconnected
    players.remove(currentPlayer) # removes client from game
    conn.close()

def master(): # Gives server vision

    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Master")

    while True:
        DISPLAY.fill((255,255,255)) # background

        for event in pygame.event.get(): # if quit is pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        for blob in blobs: # draws small edible blobs
            blob.draw(DISPLAY)

        for player in players: #Draws players
            player.draw(DISPLAY)

        s = Scoreboard(DISPLAY, WIDTH, HEIGHT, None)
        s.showNames(players) # Draws players names

        pygame.display.update()

def main():
    playerID = addBlobs(150) # Adds specified number of blobs
    start_new_thread(master, ())

    while True:
        conn, addr = s.accept() # Accepts new connections
        print('[NEW CONNECTION] at:', addr)

        start_new_thread(newPlayer, (conn, playerID)) # starts new client
        playerID += 1 # Updates player ID

if __name__ == '__main__':
    main()
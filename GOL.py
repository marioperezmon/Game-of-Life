'''
    Idea : https://www.youtube.com/watch?v=xgZuW6Jz5dc&ab_channel=NotCSV - Carlos Santana Vega
'''

import pygame
import numpy as np
import matplotlib.pyplot as plt
import time

pygame.init()

# dimensiones del juego
dim = 10

# tamanho de la pantalla
size = width, height = dim*100, dim*100

# numero de celdas
nxC = dim * 10
nyC = dim * 10

# dimensiones de cada celda
dimCW = width  / nxC
dimCH = height / nyC

# configuracion pantalla
screen = pygame.display.set_mode(size)
bg = 25, 25, 25
screen.fill(bg)

# matriz de partida; Vivas = 1; Muertas = 0
gameState = np.zeros ((nxC, nyC))
# gameState = np.random.randint (0, 2, (nxC, nyC))

# conf inicial: Automata palo
'''
gameState[20, 21] = 1;
gameState[20, 22] = 1;
gameState[20, 23] = 1;
'''

# conf inicial: Automata cohete
'''
gameState[21, 21] = 1;
gameState[22, 22] = 1;
gameState[22, 23] = 1;
gameState[21, 23] = 1;
gameState[20, 23] = 1;
'''

# para ver el estado inicial
'''
plt.matshow((gameState))
plt.show()
'''

pause = False
while 1:

    # copiar la matriz para guardar los cambios
    new_gameState = np.copy(gameState)

    # generar la matriz desde 0 para no conservar estados anteriores
    screen.fill(bg)

    # entrada por teclado
    ev = pygame.event.get()

    # sin un for de eventos pygame window falla
    for event in ev:

        # pausa al pulsar una tecla
        if event.type == pygame.KEYDOWN:
            pause = not pause

        mouseClick = pygame.mouse.get_pressed()
        #print (mouseClick) # vector (x, y, z); (0, 0, 1) = pulsacion del raton

        # si se clico el raton
        if sum(mouseClick) > 0:
            # posicion del click en pixeles y buscar la celda
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int (np.floor(posX / dimCW)), int (np.floor(posY / dimCH))

            # cambia el estado de la celda entre viva/muerta
            # new_gameState[celX, celY] = not new_gameState[celX, celY]
            # click dcho cambia a viva/izq a muerta
            new_gameState[celX, celY] = not mouseClick[2]

    # recorrer cada celda de la matriz
    for y in range(0, nyC):
        for x in range(0, nxC):

            if not pause:

                # calcular numVecinos de cada celda, con modulo para que sea toroidal
                numVecinos =    gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                                gameState[(x) % nxC,     (y - 1) % nyC] + \
                                gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                                gameState[(x - 1) % nxC, (y) % nyC] + \
                                gameState[(x + 1) % nxC, (y) % nyC] + \
                                gameState[(x - 1) % nxC, (y+1) % nyC] + \
                                gameState[(x) % nxC,     (y + 1) % nyC] + \
                                gameState[(x + 1) % nxC, (y + 1) % nyC]

                # Regla 1: Una celula muerta con exactamente 3 vecinos vivos, nace
                if gameState[x, y] == 0 and numVecinos == 3:
                    new_gameState[x, y] = 1 # proximo estado de la matriz

                # Regla 2: Una celula viva con 2 o 3 celulas vecinas vivas, sigue viva. En caso contrario, muere
                elif gameState[x, y] == 1 and (numVecinos < 2 or numVecinos > 3):
                    new_gameState[x, y] = 0 # proximo estado de la matriz

            poly = [((x) * dimCW,     (y) * dimCH),
                    ((x + 1) * dimCW, (y) * dimCH),
                    ((x + 1) * dimCW, (y + 1) * dimCH),
                    ((x) * dimCW,     (y + 1) * dimCH)]

            pygame.draw.polygon(screen, (128, 128, 128), poly, int(abs(1 - new_gameState[x, y])))

    # cargar nuevo estado de la matriz
    gameState = new_gameState
    time.sleep(0.01)

    # avance paso a paso
    '''
    plt.matshow((gameState))
    plt.show()
    '''

    pygame.display.flip()


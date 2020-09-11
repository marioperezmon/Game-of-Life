import pygame
import numpy as np
import matplotlib.pyplot as plt
import time

pygame.init()

# variable para poder aumentar la dimension facilmente
dim = 10

# tamanho de la pantalla
size = width, height = dim*100, dim*100
# size = width, height = 600, 600

#numero de celdas
nxC = dim * 10
nyC = dim * 10
# nxC = 60
# nyC = 60

# dimensiones de cada celda
dimCW = width  / nxC
dimCH = height / nyC

# color de fondo de la pantalla
bg = 25, 25, 25

# configuracion pantalla
screen = pygame.display.set_mode(size)
screen.fill(bg)

# matriz de partida; Vivas = 1; Muertas = 0
gameState = np.zeros ((nxC, nyC)) # conf vacia
# gameState = np.random.randint (0, 2, (nxC, nyC)) # conf binaria

# conf inicial: Automata palo
# gameState[20, 21] = 1;
# gameState[20, 22] = 1;
# gameState[20, 23] = 1;

# conf inicial: Automata cohete
# gameState[21, 21] = 1;
# gameState[22, 22] = 1;
# gameState[22, 23] = 1;
# gameState[21, 23] = 1;
# gameState[20, 23] = 1;

# descomentar para ver el estado inicial
# plt.matshow((gameState))
# plt.show()

# variable para pausar la ejecucion del codigo
pause = False

while 1:

    # sin un for de control de eventos, falla al abrir pygame window
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         quit()

    # guardo el estado en una copia de la matriz
    new_gameState = np.copy(gameState)

    # cada iteracion "pinta" la matriz desde 0, para no conservar los estados anteriores
    screen.fill(bg)

    # registrar eventos de teclado
    ev = pygame.event.get()

    # sin un for de control de eventos, falla al abrir pygame window
    for event in ev:
        if event.type == pygame.KEYDOWN: # pausa al pulsar una tecla
            pause = not pause

        mouseClick = pygame.mouse.get_pressed()
        print (mouseClick) # vector (x, y, z); (0, 0, 1) = pulsacion del raton

        if sum(mouseClick) > 0: # si se clicko alguna tecla del raton
            # posicion del click (en pixeles)
            posX, posY = pygame.mouse.get_pos()

            #calculo de celda en la que se cliclo
            celX, celY = int (np.floor(posX / dimCW)), int (np.floor(posY / dimCH))

            #cambiar el estado de la celda que se cliclo
            # new_gameState[celX, celY] = not new_gameState[celX, celY] # cambia el estado de la celda: viva/muerta
            new_gameState[celX, celY] = not mouseClick[2] # cambia el estado de la celda: click dcho viva / izq muerta



    # recorrer cada celda de la matriz
    for y in range(0, nyC):
        for x in range(0, nxC):

            if not pause:  # si la ejecucion no esta pausada, continua de manera natura

                # calcular numVecinos de cada celda
                # se hace el modulo para que el calculo sea toroidal
                numVecinos =    gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                                gameState[(x) % nxC,     (y - 1) % nyC] + \
                                gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                                gameState[(x - 1) % nxC, (y) % nyC] + \
                                gameState[(x + 1) % nxC, (y) % nyC] + \
                                gameState[(x - 1) % nxC, (y+1) % nyC] + \
                                gameState[(x) % nxC,     (y + 1) % nyC] + \
                                gameState[(x + 1) % nxC, (y + 1) % nyC]

                # Regla #1: Una celula muerta con exactamente 3 vecinos vivos, "nace".
                if gameState[x, y] == 0 and numVecinos == 3:
                    new_gameState[x, y] = 1 # actualizo el proximo estado de la matriz

                # Regla #2: Una celula viva con 2 o 3 celulas vecinas vivas, sigue viva. En caso contrario, muere.
                elif gameState[x, y] == 1 and (numVecinos < 2 or numVecinos > 3):
                    new_gameState[x, y] = 0 # actualizo el proximo estado de la matriz

            poly = [((x) * dimCW, (y) * dimCH),
                    ((x + 1) * dimCW,     (y) * dimCH),
                    ((x + 1) * dimCW,     (y + 1) * dimCH),
                    ((x) * dimCW, (y + 1) * dimCH)]

            pygame.draw.polygon(screen, (128, 128, 128), poly, int(abs(1 - new_gameState[x, y])))

    # cargo nuevo estado de la matriz
    gameState = new_gameState
    time.sleep(0.01)

    # descomentar para ver el cambio paso a paso
    # plt.matshow((gameState))
    # plt.show()

    pygame.display.flip()

# en ppio, no necesario el quit()
# pygame.quit()

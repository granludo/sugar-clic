# -*- coding: utf-8 -*-
import pygame
import random
#import pygtk
pygame.font.init()
from pygame.locals import *
from pygame.sprite import Sprite
from random import shuffle

class Activitat:
    def main(self,path):
        self.presionat = False
        self.salir = False
	self.i =0
        # Creem la finestra
        self.screen = pygame.display.set_mode((1200, 820))
        self.screen.fill((255,255,255),(0,600,1200,250))
        pygame.display.set_caption("Puzzle")
        #pygame.mouse.set_visible(False)

        self.screen.fill((255,255,255),(50,50,150,150))
        self.screen.fill((255,255,255),(500,50,150,150))

        
        self.seguent = True
        self.enc = 0
        self.fall = 0

        #Dibuixem les linies blanques


        self.encerts = pygame.font.Font.render(pygame.font.Font(None, 25),
                                               "Puzzle1", 1, (0,255,0), (255,255,255))

        self.fallos = pygame.font.Font.render(pygame.font.Font(None, 25),
                                               "Puzzle2", 1, (255,0,0), (255,255,255))
        
        self.screen.blit(self.encerts, (90,90))
        self.screen.blit(self.fallos, (590,90))
        


        #Fem un vector amb les posicions del puzzle i el desordenem perque lordre de les peces
        #sigui aleatori
        self.vector = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2),(3,0),
                  (3,1),(3,2),(4,0),(4,1),(4,2),(5,0),(5,1),(5,2)]

	shuffle(self.vector)
        
        

        #Fem una copia de la pantalla per no haver de copiar les peces una a una
        self.hola = self.screen.copy()


        self.temporizador = pygame.time.Clock()
	self.update2()
	
    # Bucle per col.locar cada una de les peces
    def update2(self):
	if self.salir or self.i==18:
	    #print "sortir"
	    exit()
	self.x,self.y = self.vector[self.i]
        self.seguent = True
        self.i = self.i + 1
        if self.salir or self.i==20:
            sys.exit()

	pygame.event.clear()

    # Es cridara aquesta funcio en el bucle de main de tal manera que
    # s'actualitzi la pantalla i la posicio de la fitxa
    def updating(self):
	    diccionari=dict([('encerts',0),('fallos',0),('text',"Benvingut")])
	    if not self.salir and self.seguent:
                self.screen.fill((255,255,255),(800,0,800,800))
            
                self.screen.blit(self.hola,(0,0,640,640))
                
                pos = pygame.mouse.get_pos()
                x,y = pygame.mouse.get_pos()

                if pygame.mouse.get_pressed()[0] and x > 50 and x < 200 and y>50 and y < 200:
		    return -1,diccionari
                            
                if pygame.mouse.get_pressed()[0] and x > 500 and x < 650 and y>50 and y < 200:
		    return -2,diccionari
                

                #Actualtizem la pantalla            
                pygame.display.flip()
                self.temporizador.tick(30)


                # Si sortim
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        self.salir = True

	    if not self.seguent:
            	self.hola = self.screen.copy()
            	pygame.event.clear()
		self.update2()

	    if self.salir:
		exit()
	    pygame.event.clear()
	    return 0, diccionari

if __name__ == '__main__':
	act = Activitat()
	act.main()
	while True:
		act.updating()
 

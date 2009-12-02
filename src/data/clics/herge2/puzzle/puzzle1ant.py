# -*- coding: utf-8 -*-
import pygame
import random
import pygtk
pygame.font.init()
from pygame.locals import *
from pygame.sprite import Sprite
from random import shuffle

class Peca(pygame.sprite.Sprite):

    def __init__(self, cordx, cordy, img):
	#Creem una nova pessa a partir de les coordenades
        pygame.sprite.Sprite.__init__(self)
        self.cordx = cordx
        self.cordy = cordy
        self.rect2 = pygame.Rect(cordx, cordy, 200, 200)
        self.image2 = pygame.image.load(img)
        self.image3 = pygame.transform.scale(self.image2,(1200,600))
        self.image = self.image3.subsurface(self.rect2).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(300, 620)
        self.coordenadasx = []
        self.coordenadasy = []
        self.sortir = False
        self.fallat = False
        pygame.mouse.set_pos([300,710])
	self.apretat = False

    def update(self):
        #Gestionem les tecles i variem la posicio de la pessa
        teclas = pygame.key.get_pressed()
        raton = pygame.mouse.get_pressed()

        pos = pygame.mouse.get_pos()
        self.rect.center = pos

        self.fallat = False

        if teclas[K_q] or teclas[K_ESCAPE]:
            self.sortir = True
            
        if teclas[K_LEFT] and self.rect.x>0:
            self.rect.x -= 20
        elif teclas[K_RIGHT] and self.rect.x < (1200-200):
            self.rect.x += 20
        elif teclas[K_UP] and self.rect.y > 0:
            self.rect.y -= 20
        elif teclas[K_DOWN] and self.rect.y < (600-200):
            self.rect.y += 20

        

        if teclas[K_a] or (teclas[K_SPACE] or pygame.mouse.get_pressed()[0]) and (self.rect.x > self.cordx-20 and self.rect.x < self.cordx+20 and self.rect.y > self.cordy-20 and self.rect.y<self.cordy+20) and not self.apretat:
            self.rect.x = self.cordx
            self.rect.y = self.cordy
            self.coordenadasx += [self.cordx]
            self.coordenadasy += [self.cordy]
            temporizador = pygame.time.Clock()
            return False
        
	temporizador = pygame.time.Clock()
        if pygame.mouse.get_pressed()[0] and not self.apretat:
	    self.apretat = True
            self.fallat = True
	elif not(pygame.mouse.get_pressed()[0] and self.apretat):
	    self.apretat = False

        return True

    def sortirFunc(self):
        return self.sortir

    def haFallat(self):
        return self.fallat

class Activitat:
    def main(self, path):
        self.salir = False
        self.i =0
        # Creem la finestra
        self.screen = pygame.display.get_surface()
        self.screen.fill((255,255,255),(0,600,1200,250))
        pygame.mouse.set_visible(False)

        self.seguent = True
        self.enc = 0
        self.fall = 0

        #Dibuixem les linies blanques
        for i in range(1,6):
            pygame.draw.line(self.screen,(255,255,255), (200*i,0),(200*i,800))

        for i in range(1,3):
            pygame.draw.line(self.screen,(255,255,255), (0,200*i),(1200,200*i))

	self.instruc = "Mou les peces amb el ratoli i clica a on correspongui"

        self.instruccions = pygame.font.Font.render(pygame.font.Font(None, 25),
                                               "Mou amb les fletxes del teclat i quan el tinguis col.locat presiona l'espai ", 1, (0,0,0), (255,255,255))

        self.encerts = pygame.font.Font.render(pygame.font.Font(None, 25),
                                               "Encerts = 0 ", 1, (0,255,0), (255,255,255))

        self.fallos = pygame.font.Font.render(pygame.font.Font(None, 25),
                                               "Fallades = 0 ", 1, (255,0,0), (255,255,255))
        
        self.screen.blit(self.instruccions, (560, 800))
        self.screen.blit(self.encerts, (620,710))
        self.screen.blit(self.fallos, (620,740))
        


        #Fem un vector amb les posicions del puzzle i el desordenem perque lordre de les peces
        #sigui aleatori
        self.vector = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2),(3,0),
                  (3,1),(3,2),(4,0),(4,1),(4,2),(5,0),(5,1),(5,2)]

        shuffle(self.vector)
        
        imatges = [path+'/ejemplo1.jpg']
        
        self.imatge = random.choice(imatges)

        #Imatge petita que sortira a la part de baix de la pantalla
        fondo2 = pygame.image.load(self.imatge).convert()
        self.fondo = pygame.transform.scale(fondo2,(400,180))
        

        #Fem una copia de la pantalla per no haver de copiar les peces una a una
        self.hola = self.screen.copy()

        self.temporizador = pygame.time.Clock()
	self.update2()
    
	#Bucle per colocar les peces
    def update2(self):
	if self.i<18:
		self.x,self.y = self.vector[self.i]
	        self.seguent = True
	        self.i = self.i + 1
        	#if self.salir or self.i==20:
	            #sys.exit()

	        self.pessa = Peca(self.x*200,self.y*200, self.imatge)
		pygame.event.clear()
	else:
		pygame.mouse.set_visible(True)
		self.instruc = "Molt be"

    def updating(self):
            if not self.salir and self.seguent:
                self.seguent = self.pessa.update()
                self.screen.fill((255,255,255),(800,0,800,800))
            
                self.screen.blit(self.hola,(0,0,640,640))

                if self.pessa.haFallat():
                    self.fall = self.fall +1
                    self.fallos = pygame.font.Font.render(pygame.font.Font(None, 25),
                                               "Fallades = " + str(self.fall), 1, (255,5,5), (255,255,255))
                self.screen.blit(self.fallos, (620,740))
        
                self.rectpetit = self.fondo.get_rect()
                self.rectpetit.move_ip(780, 620)
                self.screen.blit(self.fondo,self.rectpetit)
                self.screen.blit(self.pessa.image, self.pessa.rect)


                #Actualtizem la pantalla            
                pygame.display.flip()
                self.temporizador.tick(30)

                self.salir = self.pessa.sortirFunc()

                if not self.seguent:
                    self.enc = self.enc +1
                    self.encerts = pygame.font.Font.render(pygame.font.Font(None, 25),
                                               "Encerts = " + str(self.enc), 1, (0,255,0), (255,255,255))
                    self.screen.blit(self.encerts, (620,710))



                # Si sortim
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        self.salir = True
	    diccionari = dict([('encerts',self.enc),('fallos',self.fall),('text',self.instruc)])
	    if not self.seguent:
            	self.hola = self.screen.copy()
            	pygame.event.clear()
		self.update2()
		#return self.update2(),diccionari

	    if self.salir:
		exit()
	    pygame.event.clear()

	    return 0,diccionari

if __name__ == '__main__':
	act = Activitat()
	act.main()
	while True:
		act.updating()
 

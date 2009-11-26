import pygame

class ClicActivities:
    def __init__(self, path, mediaTag, settingsTag):
        self.path_to_clic = path
        self.mediaBagXML = mediaTag
        self.settingsXML = settingsTag
        
    #starts the activity declared in activityTag
    def start_activity(self, activityTag):

	# Inicialize screen and buttons of ClicXO
        self.screen = pygame.display.get_surface()
        (x,y)=self.screen.get_size()
        self.screen.fill((0,0,0),(0,0,x,y))
        self.selecciona = pygame.font.Font.render(pygame.font.Font(None, 25),
                                               "See available clics", 1, (0,0,255), (255,255,255))

        self.rectSelecciona = self.screen.blit(self.selecciona, (100, 400))
	
        next = pygame.image.load("next.png").convert()
        previous = pygame.image.load("previous.png").convert()
        self.next = pygame.transform.scale(next,(30,30))
        self.previous = pygame.transform.scale(previous,(30,30))
        
        self.rectSeguent = self.screen.blit(self.next,(350,400))
        self.rectAnterior = self.screen.blit(self.previous,(300,400))

	#Prova: mostrem per pantalla el nom de l'activitat actual de la sequencia	
        self.__paint_xml(activityTag)

        # TODO
	# Recollir parametres i class de clic_activity
	# executar activity_class.main(parametres)


    def update_activity(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
        	#Retornem -2 tractant la seguent activitat
            if(self.rectSeguent.collidepoint(pygame.mouse.get_pos())):
                return -2

	        #Retornem -3 tractant l'activitat anterior
        	if(self.rectAnterior.collidepoint(pygame.mouse.get_pos())):
		           return -3

            	#Retornem -1 perque es tracti al clic_player per tornar a comensar
            if(self.rectSelecciona.collidepoint(pygame.mouse.get_pos())):
                    return -1

            return 0

        # TODO
        # activity_class.update()
	# return resultats, temps, ...


    #Paint the name of the xml activity
    def __paint_xml(self,clic_activity):
        sel = pygame.font.Font.render(pygame.font.Font(None, 25),clic_activity.getAttribute('name'), 1, (255,255,255), (0,0,0))
        self.screen.fill((0,0,0), (50,50,200,20))
        self.screen.blit(sel, (50, 50))
                

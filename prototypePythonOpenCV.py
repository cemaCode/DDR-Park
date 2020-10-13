import time
import numpy as np 
import random
from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import cv2
import sys
import keyboard

#Initialisations PyGame 
pygame.init()
pygame.display.set_caption("Prototype DDR Park")
screen = pygame.display.set_mode((640, 480))
taille = pygame.display.Info()
fullSize = fullWidth,fullHeight = taille.current_w, taille.current_h
halfSize = halfWidth,halfHeight = fullWidth//2,fullHeight//2
Hpoint4, Hpoint2  = int(fullHeight*0.4), int(fullHeight*0.2)
Wpoint4, Wpoint2  = int(fullWidth*0.4), int(fullWidth*0.2)
s = pygame.Surface((fullWidth,fullHeight), pygame.SRCALPHA)   
s.fill((0,0,0,0))                         
pygame.font.init()
myfont = pygame.font.SysFont('verdanaprosemibold', 30)
arrUp = pygame.image.load("arrow_up.png").convert_alpha()
arrDown = pygame.image.load("arrow_down.png").convert_alpha()
arrLeft = pygame.image.load("arrow_left.png").convert_alpha()
arrRight = pygame.image.load("arrow_right.png").convert_alpha()
selectIcon  = pygame.image.load("selectCut.png").convert_alpha() 
arrUp = pygame.transform.scale(arrUp, (164,164))
arrDown =  pygame.transform.scale(arrDown,(164,164))
arrLeft =  pygame.transform.scale(arrLeft, (164,164))
arrRight =  pygame.transform.scale(arrRight, (164,164))
selectIcon =  pygame.transform.scale(selectIcon, (124,48))

#Lancement de la webcam
webcam = cv2.VideoCapture(0) 
	
#Detection du marqueur vert
def detecGreen(green_mask):
	contours, hierarchy = cv2.findContours(green_mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
	 
	for pic, contour in enumerate(contours): 
		area = cv2.contourArea(contour) 
		if(area > 300): 
			x, y, w, h = cv2.boundingRect(contour) 
			Posx = x+w//2 #Position X du centre de l'objet
			Posy = y+h//2 #Position X du centre de l'objet
			rayon = ((w+h)//2)%halfHeight//2
			return ((Posx,Posy),rayon)
	return ((1000,1000),0)

#Detection du marqueur rouge
def detecRed(red_mask):
	contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 

	for pic, contour in enumerate(contours): 
		area = cv2.contourArea(contour) 
		if(area > 300): 
			x, y, w, h = cv2.boundingRect(contour) 
			Posx = x+w//2 #Position X du centre de l'objet
			Posy = y+h//2 #Position X du centre de l'objet
			rayon = ((w+h)//2)%halfHeight//2
			return ((Posx,Posy),rayon)
	return ((1000,1000),0)

#Emulation du clavier 
def emulateur(contact):
	if (1 in contact ):
		keyboard.press('left')
		pygame.draw.rect(s,(255,0,255,192),supG)
	else:
		keyboard.release('left')	
	if (2 in contact ):
		keyboard.press('up')
		pygame.draw.rect(s,(255,255,0,192),supD)
	else:
		keyboard.release('up')	
	if (3 in contact ):
		keyboard.press('down')
		pygame.draw.rect(s,(0,255,255,192),infG)
	else:
		keyboard.release('down')	
	if (4 in contact ):
		keyboard.press('right')

		pygame.draw.rect(s,(128,255,128,192),infD)
	else:
		keyboard.release('right')	
	if (5 in contact ):
		pygame.draw.rect(s,(128,128,128,192),selRect)
		keyboard.press_and_release('enter')
		
#Dessin de la grille
def newGrid():
	global supG
	global supD
	global infG
	global infD
	global selRect
	screen.blit(s, (0,0))
	infDroitRect = pygame.Rect(Wpoint4+Wpoint2,Hpoint4+Hpoint2, fullWidth,fullHeight)#Vert (n4)
	infGaucheRect = pygame.Rect(0,Hpoint4+Hpoint2,Wpoint4,fullHeight)#Cyan (n3)
	supDroitRect = pygame.Rect(Wpoint4+Wpoint2,0,fullWidth,Hpoint4)#Jaune (n2)
	supGaucheRect = pygame.Rect(0,0,Wpoint4,Hpoint4)#Magenta (n1)
	selectRect=  pygame.Rect(Wpoint4,Hpoint4,Wpoint2,Hpoint2)#Select (n5)
	rects = [ infDroitRect,infGaucheRect,supDroitRect, supGaucheRect,selectRect]
	supG = pygame.draw.rect(s,(255,0,255,128),supGaucheRect)
	supD = pygame.draw.rect(s,(255,255,0,128),supDroitRect)
	infG = pygame.draw.rect(s,(0,255,255,128),infGaucheRect)
	infD = pygame.draw.rect(s,(100,255,100,128),infDroitRect)
	selRect = pygame.draw.rect(s,(128,128,128,128),selectRect)
	aUR = arrUp.get_rect() # n2
	aDR = arrDown.get_rect() # n3
	aLR = arrLeft.get_rect() # n1
	aRR = arrRight.get_rect() #n4
	sR = selectIcon.get_rect() #n5
	aUR.center = supD.center
	aDR.center = infG.center
	aLR.center = supG.center
	aRR.center = infD.center
	sR.center = selRect.center
	s.blit(arrUp, aUR)
	s.blit(arrDown, aDR)
	s.blit(arrLeft, aLR)
	s.blit(arrRight, aRR)
	s.blit(selectIcon,sR)
	return rects

#Detection de collison marqueur-rectancle
def collisionDetec(rects,mouse):
	contact = 0
	for rect in rects:
		if (rect.collidepoint(mouse)):
			if(rect[0]==0):
				if(rect[1]==0):
					contact = 1
				else:
					contact = 3
			elif(rect[0]==Wpoint4+Wpoint2):
				if(rect[1]==0):
					contact = 2
				else:
					contact = 4
			else:
				contact = 5
	return contact

#Lancement du feed webcam et affichage
def camRun():
	ret, frame = webcam.read()
	try:
		frame = cv2.resize(frame,(fullWidth,fullHeight), interpolation = cv2.INTER_CUBIC)
	except:
		print("Erreur: Webcam Inaccessible\n Fermez une autre fenetre qui utilise la webcam et relancez")
		quit()
	frame =cv2.flip(frame,1)
	screen.fill([0, 0, 0])
	frame = frame.swapaxes(0, 1)
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	pygame.surfarray.blit_array(screen, frame)
	return frame

#Ferme la webcam et la fenetre 
def quitAll():
	webcam.release() 
	pygame.mixer.music.stop()
	cv2.destroyAllWindows() 
	sys.exit(0)

#Page d'introduction (Titre) du jeu 'Optionel'
def gameIntro():
	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitAll()
		frame = camRun()
		largeText = pygame.font.SysFont("arial",115)
		txtInrto = largeText.render('DDR Park', True, (128,255,128))
		textRect = txtInrto.get_rect()
		textRect.center = halfSize
		screen.blit(txtInrto,textRect)
		GI = pygame.Rect(0,halfHeight,halfWidth,halfHeight)
		pygame.draw.rect(s,(255,0,255,50),textRect) #Magenta
		pygame.display.update()
		click = pygame.mouse.get_pressed()
		if click[0] == 1 :
			break

#Boucle de jeu
def gameLoop():
	webcam = cv2.VideoCapture(0) 
	Pw, Ph = 25,25
	Posx,Posy = 1000,1000
	colors = ["Jaune", "Magenta","Cyan","Vert" ]
	emplacement_temp = ""
	newCol = random.choice(colors)
	txtP= myfont.render(newCol, False, (255,255,255))
	niveau=10
	currenTime = int(time.time())
	timeLeft = currenTime+niveau
	mouse = Posx,Posy = 1000,1000
	Pw, Ph = 25,25 
	points = 0
	while(1): 
		frame = camRun()
		rects = newGrid()
		frame = frame.swapaxes(0, 1)
		HSV = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

		red_lower = np.array([164 ,188  ,80], np.uint8) 
		red_upper = np.array([255, 255 ,255], np.uint8) 
		red_mask = cv2.inRange(HSV, red_lower, red_upper)

		green_lower = np.array([ 40, 65 , 55], np.uint8) 
		green_upper = np.array([75 ,185  ,135], np.uint8) 
		green_mask = cv2.inRange(HSV, green_lower, green_upper) 
	
		kernal = np.ones((5, 5), "uint8")

		red_mask = cv2.dilate(red_mask, kernal) 
		res_red = cv2.bitwise_and(frame, frame,mask = red_mask) 
		green_mask = cv2.dilate(green_mask, kernal) 
		# res_red = cv2.bitwise_and(frame, frame,mask = red_mask) 
		Redpointeur, Redrayon = detecRed(red_mask)
		Greenpointeur, Greenrayon = detecGreen(green_mask)

		pygame.draw.circle(screen, (255, 0, 255), Redpointeur, Redrayon)
		pygame.draw.circle(screen, (128, 255, 128), Greenpointeur,Greenrayon)
		contactR = collisionDetec(rects, Redpointeur)
		contactG = collisionDetec(rects, Greenpointeur)
		contact = [contactG, contactR]

		emulateur(contact)
		pygame.display.flip()
		
		#Pour quitter appuyer sur ESC
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitAll()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE or event.key == K_q:
					quitAll()
#gameIntro()
#Lancement du jeu
gameLoop()

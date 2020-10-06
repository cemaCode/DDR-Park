import time
import numpy as np 
from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import cv2
import sys

#initialise PyGame
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
screen = pygame.display.set_mode((640, 480))
taille = pygame.display.Info()
fullWidth,fullHeight = taille.current_w, taille.current_h
halfWidth,halfHeight = fullWidth//2,fullHeight//2
s = pygame.Surface((fullWidth,fullHeight), pygame.SRCALPHA)   
s.fill((0,0,0,0))                         

#Initialise variables et capture
webcam = cv2.VideoCapture(0) 
Posx,Posy = 1000,1000
Pw, Ph = 25,25

#Dessin de la grille
def dessinerGrille():
	#Dessin de la croix
	pygame.draw.line(screen,(255,255, 255), (0,halfHeight),(fullWidth,halfHeight))
	pygame.draw.line(screen,(255,255, 255), (halfWidth,fullHeight),(halfWidth,0))
	#Dessin des rectangles
	GS= pygame.Rect(0,0,halfWidth,halfHeight)
	GI = pygame.Rect(0,halfHeight,halfWidth,halfHeight)
	pygame.draw.rect(s,(255,255,0,50),GS) #Jaune
	pygame.draw.rect(s,(255,0,255,50),GI) #Magenta
	DS= pygame.Rect(halfWidth,0,fullWidth,halfHeight)
	DI = pygame.Rect(halfWidth,halfHeight,fullWidth,halfHeight)
	pygame.draw.rect(s,(0,255,255,50),DS)	#Cyan
	pygame.draw.rect(s,(128,255,128,50),DI) #Vert

#Affichage de la position du marqueur
def afficherPosition():
	emplacement = ""
	if((Posx>0 and Posx<fullWidth) and (Posy>0 and Posy <fullHeight) and emplacement == ""):
		if(Posy > halfHeight):
			print("\nPartie inférieure")
			emplacement+= "I"
		elif(Posy < halfHeight):
			print("\nPartie supperieur")
			emplacement+= "S"
		if(Posx >halfWidth):
			print("Cote droit\n")
			emplacement+= "D"
		elif(Posx <halfWidth) :
			print("Cote gauche\n")
			emplacement+= "G"
		if emplacement == "IG":
			print("zone magenta")
		elif emplacement == "ID":
			print("zone verte")
		elif emplacement == "SG":
			print("zone jaune")
		elif emplacement == "SD":
			print("zone cyan") 
		jouerSon(emplacement);
	return emplacement

#Jouer le son correspondant	
def jouerSon(emplacement):
	if(emplacement_temp!=emplacement):
		if emplacement == "IG":
			pygame.mixer.music.load('red.mp3')
			pygame.mixer.music.play()
		if emplacement == "ID":
			pygame.mixer.music.load('green.mp3')
			pygame.mixer.music.play()
		if emplacement == "SG":
			pygame.mixer.music.load('yellow.mp3')
			pygame.mixer.music.play()
		if emplacement == "SD":
			pygame.mixer.music.load('blue.mp3')
			pygame.mixer.music.play()

emplacement_temp = ""
while(1): 
	ret, frame = webcam.read()
	frame = cv2.resize(frame,(fullWidth,fullHeight), interpolation = cv2.INTER_CUBIC) 
	frame =cv2.flip(frame,1)
	screen.fill([0, 0, 0])
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#Masque rouge
	HSV = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV) 	
	red_lower = np.array([164 ,188  ,80], np.uint8) 
	red_upper = np.array([255, 255 ,255], np.uint8) 
	red_mask = cv2.inRange(HSV, red_lower, red_upper) 	
	kernal = np.ones((5, 5), "uint8") 	
	red_mask = cv2.dilate(red_mask, kernal) 
	res_red = cv2.bitwise_and(frame, frame,mask = red_mask) 
	contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
	
	#Incrustation du feed webcam sur l'écran
	frame = frame.swapaxes(0, 1)
	pygame.surfarray.blit_array(screen, frame)
	screen.blit(s, (0,0))

	dessinerGrille()

	#Pour chaque objet detecté
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour) 
		if(area > 300): #Si la taille de l'obj > 300 px
			x, y, w, h = cv2.boundingRect(contour) 
			Posx = x+w//2 #Position X du centre de l'objet
			Posy = y+h//2 #Position X du centre de l'objet
			Pw = w #Largeur de l'obj
			Ph = h #Hauteur de l'obj
			rayon =((Pw+Ph)//2)%halfHeight//2 #Le rayon change avec la distance 
			pygame.draw.circle(screen, (0, 0, 255), (Posx, Posy), rayon)
			emplacement_temp = afficherPosition()

	pygame.display.update()
	
	#Pour quitter appuyer sur ESC
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	    	webcam.release() 
	    	pygame.mixer.music.stop()
	    	cv2.destroyAllWindows() 
	    	sys.exit(0)
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE or event.key == K_q:
	        	webcam.release() 
	        	pygame.mixer.music.stop()
	        	cv2.destroyAllWindows() 
	        	sys.exit(0)

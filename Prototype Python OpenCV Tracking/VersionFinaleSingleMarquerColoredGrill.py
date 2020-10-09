import time
import numpy as np 
from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import cv2
import sys

#initialise PyGame
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
# pygame.font.init() 
#Transparence
screen = pygame.display.set_mode((640, 480))
# sW,sH = 1280,720
# screen = pygame.display.set_mode([sW,sH])
val = pygame.display.Info()
sW,sH = val.current_w, val.current_h
# print(sW,sH)
s = pygame.Surface((sW,sH), pygame.SRCALPHA)   
s.fill((0,0,0,0))                         

#Initialise variables et capture
webcam = cv2.VideoCapture(0) 
# webcam.set(3,sH)
# webcam.set(4,sW)
Posx,Posy = 1000,1000
Pw, Ph = 25,25

def dessinerGrille():
	##Grille partie suppérieure 
	pygame.draw.line(screen,(255,255, 255), (0,mH),(sW,mH))
	# gg = pygame.Rect(0,0,mW//2,mH)
	# pygame.draw.rect(s,(255,255,0,50),gg)
	# gm = pygame.Rect((mW//2), 0,(mW//2),mH )
	# pygame.draw.rect(s,(255,0,255,50),gm) #Magenta
	# dm= pygame.Rect(mW,0,mW//2,mH)
	# dd = pygame.Rect(mW+0.5*mW,0,sW,mH)
	# pygame.draw.rect(s,(0,255,255,50),dm)	#Cyan
	# pygame.draw.rect(s,(128,255,128,50),dd) #Vert

	# pygame.draw.line(screen,(255,255, 255), (mW,mH),(mW,0))
	pygame.draw.line(screen,(255,255, 255), (mW,sH),(mW,0))
	# pygame.draw.line(screen,(255,255, 255), (mW//2,mH),(mW//2,0))
	# pygame.draw.line(screen,(255,255, 255), (mW+0.5*mW,mH),(mW+0.5*mW,0))
	# pygame.draw.line(screen,(255,255, 255), (0,mH),(sW,mH))

	GS= pygame.Rect(0,0,mW,mH)
	GI = pygame.Rect(0,mH,mW,mH)
	pygame.draw.rect(s,(255,255,0,50),GS) #Jaune
	pygame.draw.rect(s,(255,0,255,50),GI) #Magenta
	DS= pygame.Rect(mW,0,sW,mH)
	DI = pygame.Rect(mW,mH,sW,mH)
	pygame.draw.rect(s,(0,255,255,50),DS)	#Cyan
	pygame.draw.rect(s,(128,255,128,50),DI) #Vert


def afficherPosition():
	emplacement = ""
	if((Posx>0 and Posx<sW) and (Posy>0 and Posy <sH) and emplacement == ""):
		if(Posy > mH):
			print("\nPartie inférieure")
			emplacement+= "I"
		elif(Posy < mH):
			print("\nPartie supperieur")
			emplacement+= "S"
		if(Posx >mW):
			print("Cote droit\n")
			emplacement+= "D"
		elif(Posx <mW) :
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
def jouerSon(emplacement):
	if(emplacement_temp!=emplacement):
		if emplacement == "IG":
			pygame.mixer.music.load('red.mp3')
			pygame.mixer.music.play()
			# time.sleep(0.5)
			# pygame.mixer.music.stop()
		if emplacement == "ID":
			pygame.mixer.music.load('green.mp3')
			pygame.mixer.music.play()
			# time.sleep(0.5)
			# pygame.mixer.music.stop()
		if emplacement == "SG":
			pygame.mixer.music.load('yellow.mp3')
			pygame.mixer.music.play()
			# time.sleep(0.5)
			# pygame.mixer.music.stop()
		if emplacement == "SD":
			pygame.mixer.music.load('blue.mp3')
			pygame.mixer.music.play()
			# time.sleep(0.5)
			# pygame.mixer.music.stop()
		# pygame.mixer.music.stop()
		# pygame.mixer.music.play(-1,0.0)

emplacement_temp = ""
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.play(-1,0.0)
# pygame.mixer.music.play(-1, 0.0)
while(1): 
	# screen = pygame.display.set_mode((1280, 720))
	# print(sW,sH)
	val = pygame.display.Info()
	sW,sH = val.current_w, val.current_h
	mW = sW//2
	mH= sH//2
	# print(sW,sH)
	#recuperation de la video 
	ret, frame = webcam.read()
	frame = cv2.resize(frame,(sW,sH), interpolation = cv2.INTER_CUBIC) 
	# print(frame.shape[:2])
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
	frame = frame.swapaxes(0, 1)
	pygame.surfarray.blit_array(screen, frame)
	screen.blit(s, (0,0))
	dessinerGrille()
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour) 
		if(area > 300): 
			x, y, w, h = cv2.boundingRect(contour) 
			Posx = x+w//2#Double / for euclidian division
			Posy = y+h//2
			Pw = w
			Ph = h
			rayon =((Pw+Ph)//2)%mH//2
			pygame.draw.circle(screen, (0, 0, 255), (Posx, Posy), rayon)
			emplacement_temp = afficherPosition()
			# myfont = pygame.font.SysFont('Comic Sans MS', 30)
			# textsurface = myfont.render(emplacement_temp, False, (0, 0, 0))
			# screen.blit(textsurface,(Posx,Posy))
	pygame.display.update()
	frame = frame.swapaxes(0, 1)
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

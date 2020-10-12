import time
import numpy as np 
import random
from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import cv2
import sys
import keyboard
# from pynput.keyboard import Key, Controller
# clavier = Controller()
#initialise PyGame
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
arrUp = pygame.transform.scale(arrUp, (164,164))
arrDown =  pygame.transform.scale(arrDown,(164,164))
arrLeft =  pygame.transform.scale(arrLeft, (164,164))
arrRight =  pygame.transform.scale(arrRight, (164,164))

#Initialise variables et capture
webcam = cv2.VideoCapture(0) 
Posx,Posy = 1000,1000
Pw, Ph = 25,25
colors = ["Jaune", "Magenta","Cyan","Vert" ]
points = 0



	
def detecGreen(green_mask):
	contours, hierarchy = cv2.findContours(green_mask, 
										   cv2.RETR_TREE, 
										   cv2.CHAIN_APPROX_SIMPLE) 
	  
	for pic, contour in enumerate(contours): 
		area = cv2.contourArea(contour) 
		if(area > 300): 
			x, y, w, h = cv2.boundingRect(contour) 
			Posx = x+w//2 #Position X du centre de l'objet
			Posy = y+h//2 #Position X du centre de l'objet
			rayon = ((w+h)//2)%halfHeight//2
			return ((Posx,Posy),rayon)
	return ((1000,1000),0)

def detecRed(red_mask):
	contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
	# print(contours)
	for pic, contour in enumerate(contours): 
		area = cv2.contourArea(contour) 
		if(area > 300): 
			print("detected red")
			x, y, w, h = cv2.boundingRect(contour) 
			Posx = x+w//2 #Position X du centre de l'objet
			Posy = y+h//2 #Position X du centre de l'objet
			rayon = ((w+h)//2)%halfHeight//2
			# text = str(x)+","+str(y)  
			# cv2.putText(imageFrame, text , (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255)) 
			return ((Posx,Posy),rayon)
	return ((1000,1000),0)
# def is_pressed():
# 	left = keyboard.is_pressed('left')
# 	right = keyboard.is_pressed('right')
# 	up = keyboard.is_pressed('up')
# 	down = keyboard.is_pressed('down')
# 	print("Left is : {0}\nRight is : {1}\nUp is : {2}\nDown is : {3}\n".format(left, right, up, down))
def emulateur(contact):
	if (1 in contact ):
		keyboard.press('left')
	else:
		keyboard.release('left')	
	if (2 in contact ):
		keyboard.press('up')
	else:
		keyboard.release('up')	
	if (3 in contact ):
		keyboard.press('down')
	else:
		keyboard.release('down')	
	if (4 in contact ):
		keyboard.press('right')
	else:
		keyboard.release('right')	
	if (5 in contact ):
		keyboard.press_and_release('enter')
	# if(contact[0]!= 0 and contact[1]!= 0):
	# 	print("entered if ")
	# 	if(1 in contact):
	# 		keyboard.press('left')
	# 		print("pressed left\n")
	# 	elif(2 in contact):
	# 		keyboard.press('up')
	# 	elif(3 in contact):
	# 		keyboard.press('down')
	# 	elif(4 in contact):
	# 		keyboard.press('right')
	# 	elif(5 in contact):
	# 		keyboard.press('enter')
	# 	elif(1 not in contact ):
	# 		keyboard.release('left')
	# 		print("released left\n")
	# 	elif(2 not in contact):
	# 		keyboard.release('up')
	# 	elif(3 not in contact ):
	# 		keyboard.release('down')
	# 	elif(4 not in contact):
	# 		keyboard.release('right')
	# 	elif(5 not in contact ):
	# 		keyboard.release('enter')
	# else:
	# 	# print("Contact equal [0,0] at ", contact)
	# 	# is_pressed()
	# 	print("entered else, contact is :",contact)
	# 	if(keyboard.is_pressed('left')):
	# 		keyboard.release('left')
	# 		print("released left in big else\n")
	# 	if(keyboard.is_pressed('up')):
	# 		keyboard.release('up')
	# 	if(keyboard.is_pressed('down')):
	# 		keyboard.release('down')
	# 	if(keyboard.is_pressed('right')):
	# 		keyboard.release('right')
	# 	if(keyboard.is_pressed('enter')):
	# 		keyboard.release('enter')
		
		
		
		
#Dessin de la grille
# def dessinerGrille():
	# #Dessin de la croix
	# pygame.draw.line(screen,(255,255, 255), (0,halfHeight),(fullWidth,halfHeight))
	# pygame.draw.line(screen,(255,255, 255), (halfWidth,fullHeight),(halfWidth,0))
	# #Dessin des rectangles
	# txtJ = myfont.render('Jaune', True, (255,255,0))
	# txtM = myfont.render('Magenta', True, (255,0,255))
	# txtC = myfont.render('Cyan', True, (0,255,255))
	# txtV = myfont.render('Vert', True, (128,255,128))
	# GS= pygame.Rect(0,0,halfWidth,halfHeight)
	# GI = pygame.Rect(0,halfHeight,halfWidth,halfHeight)
	# pygame.draw.rect(s,(255,255,0,50),GS) #Jaune
	# pygame.draw.rect(s,(255,0,255,50),GI) #Magenta
	# screen.blit(txtJ,(GS[:2]))
	# screen.blit(txtM,(GI[:2]))
	# DS= pygame.Rect(halfWidth,0,fullWidth,halfHeight)
	# DI = pygame.Rect(halfWidth,halfHeight,fullWidth,halfHeight)
	# pygame.draw.rect(s,(0,255,255,50),DS)	#Cyan
	# pygame.draw.rect(s,(128,255,128,50),DI) #Vert
	# screen.blit(txtC,(DS[:2]))
	# screen.blit(txtV,(DI[:2]))
def newGrid():
	# screen.fill((255, 255, 255))
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
	pygame.draw.rect(s,(128,128,128,128),selectRect)
	aUR = arrUp.get_rect() # n2
	aDR = arrDown.get_rect() # n3
	aLR = arrLeft.get_rect() # n1
	aRR = arrRight.get_rect() #n4
	aUR.center = supD.center
	aDR.center = infG.center
	aLR.center = supG.center
	aRR.center = infD.center
	s.blit(arrUp, aUR)
	s.blit(arrDown, aDR)
	s.blit(arrLeft, aLR)
	s.blit(arrRight, aRR)
	return rects
#Affichage de la position du marqueur
def collisionDetec(rects,mouse):
	contact = 0
	for rect in rects:
		if (rect.collidepoint(mouse)):
			if(rect[0]==0):
				if(rect[1]==0):
					contact = 1
					# for x in range(1000):
						# keyboard.press("left")
					# keyboard.release("left")
				else:
					contact = 3
					# keyboard.press("down")
			elif(rect[0]==Wpoint4+Wpoint2):
				if(rect[1]==0):
					contact = 2
					# keyboard.press("up")
				else:
					contact = 4
					# keyboard.press("right")
			else:
				contact = 5
				# keyboard.press("enter")
	return contact
		# else:
		# 	[print("\n") for x in range(10)]
def afficherPosition(Posx,Posy):
	emplacement = ""
	couleur = ""
	if((Posx>0 and Posx<fullWidth) and (Posy>0 and Posy <fullHeight) and emplacement == ""):
		if(Posy > halfHeight):
			# print("\nPartie inférieure")
			emplacement+= "I"
		elif(Posy < halfHeight):
			# print("\nPartie supperieur")
			emplacement+= "S"
		if(Posx >halfWidth):
			# print("Cote droit\n")
			emplacement+= "D"
		elif(Posx <halfWidth) :
			# print("Cote gauche\n")
			emplacement+= "G"
		if emplacement == "IG":
			# print("zone magenta")
			couleur = "Magenta"
		elif emplacement == "ID":
			# print("zone verte")
			couleur = "Vert"
		elif emplacement == "SG":
			# print("zone jaune")
			couleur = "Jaune"
		elif emplacement == "SD":
			# print("zone cyan") 
				couleur = "Cyan"
	return emplacement, couleur
#Jouer le son correspondant	
def jouerSon(emplacement_temp,emplacement):
	# pygame.mixer.music.stop()
	if(emplacement_temp!=emplacement):
		if emplacement == "IG":
			keyboard.press_and_release('left')
			# time.sleep(2)
			pygame.mixer.music.load('red.mp3')
			pygame.mixer.music.play()
			# keyboard.release('up')
			keyboard.release('down')
		if emplacement == "ID":
			keyboard.press('down')
			# time.sleep(0.2)
			# keyboard.release('down')
			keyboard.release('up')
			pygame.mixer.music.load('green.mp3')
			pygame.mixer.music.play()
		if emplacement == "SG":
			keyboard.press('left')
			# time.sleep(0.2)
			pygame.mixer.music.load('yellow.mp3')
			pygame.mixer.music.play()
			# keyboard.release('left')
		if emplacement == "SD":
			keyboard.press('up')
			# time.sleep(0.2)
			pygame.mixer.music.load('blue.mp3')
			pygame.mixer.music.play()
			# keyboard.release('up')

emplacement_temp = ""	

newCol = random.choice(colors)

txtP= myfont.render(newCol, False, (255,255,255))
niveau=10
currenTime = int(time.time())
timeLeft = currenTime+niveau

def camRun():
	ret, frame = webcam.read()
	frame = cv2.resize(frame,(fullWidth,fullHeight), interpolation = cv2.INTER_CUBIC) 
	frame =cv2.flip(frame,1)
	screen.fill([0, 0, 0])
	frame = frame.swapaxes(0, 1)
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	pygame.surfarray.blit_array(screen, frame)
	return frame

def gameIntro():
	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		frame = camRun()
		largeText = pygame.font.SysFont("arial",115)

		txtInrto = largeText.render('DDR Park', True, (128,255,128))
		textRect = txtInrto.get_rect()
		textRect.center = halfSize
		screen.blit(txtInrto,textRect)
		GI = pygame.Rect(0,halfHeight,halfWidth,halfHeight)
		pygame.draw.rect(s,(255,0,255,50),textRect) #Magenta
		click = pygame.mouse.get_pressed()
		if click[0] == 1 :
			break
		pygame.display.update()


def gameLoop():
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
		# dessinerGrille()
		rects = newGrid()
		frame = frame.swapaxes(0, 1)
		HSV = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

		red_lower = np.array([164 ,188  ,80], np.uint8) 
		red_upper = np.array([255, 255 ,255], np.uint8) 
		red_mask = cv2.inRange(HSV, red_lower, red_upper)

		# green_lower = np.array([ 30, 140 , 40], np.uint8) 
		# green_upper = np.array([ 50 ,255  ,75], np.uint8) 
		green_lower = np.array([ 40, 65 , 55], np.uint8) 
		green_upper = np.array([75 ,185  ,135], np.uint8) 
		green_mask = cv2.inRange(HSV, green_lower, green_upper) 
	
		kernal = np.ones((5, 5), "uint8") 	
		red_mask = cv2.dilate(red_mask, kernal) 
		res_red = cv2.bitwise_and(frame, frame,mask = red_mask) 
		green_mask = cv2.dilate(green_mask, kernal) 
		# res_red = cv2.bitwise_and(frame, frame,mask = red_mask) 
		Redpointeur, Redrayon = detecRed(green_mask)
		Greenpointeur, Greenrayon = detecGreen(red_mask)

		# contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
		# for pic, contour in enumerate(contours):
		# 	area = cv2.contourArea(contour) 
		# 	if(area > 300): #Si la taille de l'obj > 300 px
		# 		x, y, w, h = cv2.boundingRect(contour) 
		# 		Posx = x+w//2 #Position X du centre de l'objet
		# 		Posy = y+h//2 #Position X du centre de l'objet
		# 		pointeur = (Posx,Posy)
		# 		# print(pointeur)
		# 		Pw = w #Largeur de l'obj
		# 		Ph = h #Hauteur de l'obj
		# 		rayon =((Pw+Ph)//2)%halfHeight//2 #Le rayon change avec la distance 
		pygame.draw.circle(screen, (0, 0, 255), Redpointeur, Redrayon)
		pygame.draw.circle(screen, (0, 255, 255), Greenpointeur,Greenrayon)
		contactR = collisionDetec(rects, Redpointeur)
		contactG = collisionDetec(rects, Greenpointeur)
		contact = [contactG, contactR]
		# print(contact)
		# print("contactRouge: {0} \n et contacVert: {1}".format(contactR,contactG))
		# print(contact)

		emulateur(contact)
		# emplacement, color = afficherPosition(Posx,Posy)
		# txtM= myfont.render(color, True, (255,255,255))
		# screen.blit(txtM,Redpointeur)
		# jouerSon(emplacement_temp, emplacement);
		# emplacement_temp = emplacement
		# if(newCol==color):
		# 			timeLeft= int(time.time())+niveau
		# 			points+=1
		# 			newCol = random.choice(colors) 
	
		# screen.blit(txtP,(halfWidth-50,halfHeight-50))
		# currenTime = int(time.time())
		# if(currenTime == timeLeft):
		# 	currenTime = int(time.time())
		# 	newCol = random.choice(colors)
		# 	timeLeft = currenTime+niveau

		# txtP= myfont.render(newCol, True, (255,255,255))
	
		pygame.display.flip()
		
		#Pour quitter appuyer sur ESC
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				webcam.release() 
				pygame.mixer.music.stop()
				cv2.destroyAllWindows() 
				sys.exit(0)
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE or event.key == K_q:
					print("Vous avez marqué",points,"points")
					webcam.release() 
					pygame.mixer.music.stop()
					cv2.destroyAllWindows() 
					sys.exit(0)
# gameIntro()
gameLoop()

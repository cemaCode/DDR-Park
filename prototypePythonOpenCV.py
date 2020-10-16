import numpy as np 
from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import cv2
import sys
import keyboard

#Initialisations PyGame 
pygame.init()
pygame.display.set_caption("Prototype DDR Park")
icon  = pygame.image.load("iconF.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((640, 480))
taille = pygame.display.Info()
fullSize = fullWidth,fullHeight = taille.current_w, taille.current_h
halfSize = halfWidth,halfHeight = fullWidth//2,fullHeight//2
Hpoint4, Hpoint2  = int(fullHeight*0.4), int(fullHeight*0.2)
Wpoint4, Wpoint2  = int(fullWidth*0.4), int(fullWidth*0.2)
s = pygame.Surface((fullWidth,fullHeight), pygame.SRCALPHA)   
arrUp = pygame.image.load("arrow_up.png").convert_alpha()
arrDown = pygame.image.load("arrow_down.png").convert_alpha()
arrLeft = pygame.image.load("arrow_left.png").convert_alpha()
arrRight = pygame.image.load("arrow_right.png").convert_alpha()
selectIcon  = pygame.image.load("startw.png").convert_alpha() 
# selectIcon  = pygame.image.load("selectCut.png").convert_alpha() 
arrUp = pygame.transform.scale(arrUp, (164,164))
arrDown =  pygame.transform.scale(arrDown,(164,164))
arrLeft =  pygame.transform.scale(arrLeft, (164,164))
arrRight =  pygame.transform.scale(arrRight, (164,164))
# selectIcon =  pygame.transform.scale(selectIcon, (124,48))
selectIcon =  pygame.transform.scale(selectIcon, (130,51))

#Lancement de la webcam
webcam = cv2.VideoCapture(0) 

def calibrate():
	from color_tracker import WebCamera, HSVColorRangeDetector
	
	cam  = WebCamera(video_src = 0)
	cam.start_camera()
	detector = HSVColorRangeDetector(camera= cam)
	low, up, kern = detector.detect()
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
	w4 = fullWidth//6
	h4 = fullHeight//6
	#DDR MAT / CROSS STYLE
	"""
	infDroitRect = pygame.Rect(w4*4, h4*2, w4*2+4, h4*2) # Right 
	infGaucheRect = pygame.Rect(w4*2,h4*4, w4*2,h4*2) # Down
	supDroitRect = pygame.Rect(w4*2,0, w4*2,h4*2) # Up
	supGaucheRect = pygame.Rect(0, h4*2, w4*2, h4*2) # Left
	"""
	# DDR MAT / CROSS STYLE *SPACED*
	"""
	infDroitRect = pygame.Rect(Wpoint4+Wpoint2*2, h4*2, w4*2+4, h4*2) # Right 
	infGaucheRect = pygame.Rect(w4*2,h4*5, w4*2,h4*2) # Down
	supDroitRect = pygame.Rect(w4*2,0, w4*2,Hpoint2) # Up
	supGaucheRect = pygame.Rect(0, h4*2, Wpoint2, h4*2) # Left
	"""
	#CLASSIC 4 CORNERS BIG STYLE
	"""
	infDroitRect = pygame.Rect(Wpoint4+Wpoint2,Hpoint4+Hpoint2, fullWidth,fullHeight)#Vert (n4)
	infGaucheRect = pygame.Rect(0,Hpoint4+Hpoint2,Wpoint4,fullHeight)#Cyan (n3)
	supDroitRect = pygame.Rect(Wpoint4+Wpoint2,0,fullWidth,Hpoint4)#Jaune (n2)
	supGaucheRect = pygame.Rect(0,0,Wpoint4,Hpoint4)#Magenta (n1)
	"""
	#SMALL / FAR 4 CORNERS STYLE
	"""
	infDroitRect = pygame.Rect(Wpoint4+Wpoint4,Hpoint4+Hpoint4, fullWidth,fullHeight)#Vert (n4)
	infGaucheRect = pygame.Rect(0,Hpoint4+Hpoint4,Wpoint2,fullHeight)#Cyan (n3)
	supDroitRect = pygame.Rect(Wpoint4+Wpoint4,0,fullWidth,Hpoint2)#Jaune (n2)
	supGaucheRect = pygame.Rect(0,0,Wpoint2,Hpoint2)#Magenta (n1)
	"""
	#TOP SLAB STYLE
	# """
	infDroitRect = pygame.Rect(Wpoint2,0, Wpoint2,h4*2)#Vert (n4) (Right/Droite ->)
	infGaucheRect = pygame.Rect(Wpoint2*3,0,Wpoint2,h4*2)#Cyan (n3) (Down/Bas)
	supDroitRect = pygame.Rect(Wpoint2*4,0,Wpoint2,h4*2)#Jaune (n2)(up/Haut î)
	supGaucheRect = pygame.Rect(0,0,Wpoint2,h4*2)#Magenta (n1) (Left/Gauche <- )
	# """
	#BOTTOM SLAB STYLE
	"""
	infDroitRect = pygame.Rect(Wpoint2,Hpoint2*3, Wpoint2,Hpoint4	)#Vert (n4) (Right/Droite ->)
	infGaucheRect = pygame.Rect(Wpoint2*3,Hpoint2*3,Wpoint2,Hpoint4)#Cyan (n3) (Down/Bas)
	supDroitRect = pygame.Rect(Wpoint2*4,Hpoint2*3,Wpoint2,Hpoint4)#Jaune (n2)(up/Haut î)
	supGaucheRect = pygame.Rect(0,Hpoint2*3,Wpoint2,Hpoint4)#Magenta (n1) (Left/Gauche <- )
	"""
	#4 CORNER STYLE *DIFFERENT ARROW LAYOUT* 
	"""
	infDroitRect = pygame.Rect(0,Hpoint2*3,Wpoint4,Hpoint4)#Vert (n4) (Right/Droite ->)
	infGaucheRect = pygame.Rect(Wpoint2*3,Hpoint2*3,Wpoint4,Hpoint4)#Cyan (n3) (Down/Bas)
	supDroitRect = pygame.Rect(Wpoint2*3,0,Wpoint4,Hpoint4)#Jaune (n2)(up/Haut î)
	supGaucheRect = pygame.Rect(0,0,Wpoint4,Hpoint4)#Magenta (n1) (Left/Gauche <- )
	"""
	selectRect=  pygame.Rect(Wpoint4,Hpoint4,Wpoint2,Hpoint2)#Select (n5)
	rects = [ supGaucheRect,supDroitRect,infGaucheRect, infDroitRect,selectRect] # L'ordre est imporatant
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
	for i, rect in enumerate(rects):
		if (rect.collidepoint(mouse)):
			if(rect==rects[i]):
				contact = i+1
	return contact

#Lancement du feed webcam et affichage
def camRun():
	ret, frame = webcam.read()
	frame = cv2.resize(frame,(fullWidth,fullHeight), interpolation = cv2.INTER_CUBIC)
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
	starter = pygame.image.load("startw.png").convert_alpha()
	starter =  pygame.transform.scale(starter, (130,51))
	intro = True
	while intro:
		inSurf = pygame.Surface(fullSize, pygame.SRCALPHA)
		inSurf.fill((128,128,128))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitAll()
		btns = pygame.Rect(10,340,140,100)
		btns2 = pygame.Rect(140+10+10,340,140,100)
		btns3 = pygame.Rect(140*2+10*3,340,140,100)
		btns4 = pygame.Rect(140*3+10*4,340,140,100)
		pygame.draw.rect(inSurf,(100,100,100,50),btns)
		pygame.draw.rect(inSurf,(100,100,100,50),btns2)
		pygame.draw.rect(inSurf,(100,100,100,50),btns3)
		pygame.draw.rect(inSurf,(100,100,100,50),btns4)
		largeText = pygame.font.SysFont("arial",115)
		btnTxt = pygame.font.SysFont("arial", 35)
		txtLayout = btnTxt.render('Interface', True, (200,200,200) )
		btnLayouytRect = txtLayout.get_rect()
		btnLayouytRect.center = btns.center
		txtSongs = btnTxt.render('Chansons', True, (200,200,200) )
		btnSongsRect = txtSongs.get_rect()
		btnSongsRect.center = btns2.center
		txtInrto = largeText.render('DDR-Park', True, (200,200,200))
		textRect = txtInrto.get_rect()
		textRect.center = (halfWidth,halfHeight-100)
		pygame.draw.rect(inSurf,(100,100,100,50),textRect) #Magenta
		
		
		# screen.blit(starter,(100,100) )
		screen.blit(inSurf,(0,0))
		screen.blit(txtInrto,textRect)
		screen.blit(txtLayout,btnLayouytRect)
		screen.blit(txtSongs,btnSongsRect)
		pygame.display.update()
		click = pygame.mouse.get_pressed()
		if click[0] == 1 :
			break

#Boucle de jeu
def gameLoop():
	webcam = cv2.VideoCapture(0) 
	Pw, Ph = 25,25
	Posx,Posy = 1000,1000
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
# gameIntro()
#Lancement du jeu
gameLoop()

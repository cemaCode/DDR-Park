#Simple pygame program
import time
import keyboard 
# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([640, 480])
screen.fill((255,255,255))
size = height, width = 480, 640
halfsize = halfWidth,halfHeight  =  width//2,height//2  
print(halfsize)
Hpoint4, Hpoint2 =  int(height*0.4), int(height*0.2) 
Wpoint4, Wpoint2 =  int(width*0.4) ,int(width*0.2)
print(Hpoint4, Hpoint2,Wpoint4, Wpoint2) 
def collisionDetec(rects):
    color = ""
    for rect in rects:
        if (rect.collidepoint(mouse) and pygame.mouse.get_focused()):
            if(rect[0]==0):
                print("Gauche")
                if(rect[1]==0):
                    print("Supérieur")
                    color = ""
                else:
                    print("Inférieur")
                    color = ""
            elif(rect[0]==Wpoint4+Wpoint2):
                print("Droite")

                if(rect[1]==0):
                    print("Supérieur")
                    color = ""
                else:
                    print("Inférieur")
                    color = ""
            else:
                print("Select")
            print("\n") 
def newGrid():
    screen.fill((255, 255, 255))
    infDroitRect = pygame.Rect(Wpoint4+Wpoint2,Hpoint4+Hpoint2, width,height)
    infGaucheRect = pygame.Rect(0,Hpoint4+Hpoint2,Wpoint4,height)
    supDroitRect = pygame.Rect(Wpoint4+Wpoint2,0,width,Hpoint4)
    supGaucheRect = pygame.Rect(0,0,Wpoint4,Hpoint4)
    selectRect=  pygame.Rect(Wpoint4,Hpoint4,Wpoint2,Hpoint2)
    rects = [ infDroitRect,infGaucheRect,supDroitRect, supGaucheRect,selectRect]
    pygame.draw.rect(screen,(255,0,255),supGaucheRect)
    pygame.draw.rect(screen,(255,255,0),supDroitRect)
    pygame.draw.rect(screen,(0,255,255),infGaucheRect)
    pygame.draw.rect(screen,(100,255,100),infDroitRect)
    pygame.draw.rect(screen,(128,128,128),selectRect)
    pygame.display.flip()
    return rects
# Run until the user asks to quit
running = True
while running:
    mouse = pygame.mouse.get_pos()
    # rects = newGrid()
    # collisionDetec(rects)
    if (mouse >= (625,465)):
        mouse = halfsize
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    # Fill the background with white


        else:
            print("\n")
    # Draw a solid blue circle in the center
    # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
    # pygame.mouse.set_visible(False)
    # x = pygame.mouse.get_pos()[0]
    # y = pygame.mouse.get_pos()[1]
    # pygame.draw.circle(screen, (0, 0, 255), (x, y), 75)

    # # Flip the display
# Done! Time to quit.
# newGrid()
pygame.quit()

# //////Layers 
# import pygame
# pygame.init()
# # import openCv_tester
# screen = pygame.display.set_mode((300, 300))

# class Actor(pygame.sprite.Sprite):
#     def __init__(self, group, color, layer, pos):
#         self.image = pygame.Surface((30, 30))
#         self.image.fill(color)
#         self.rect = self.image.get_rect(center=pos)
#         self._layer = layer
#         pygame.sprite.Sprite.__init__(self, group)

# group = pygame.sprite.LayeredUpdates()
# Actor(group, (255, 255, 255,0), 0, (100, 100))#White
# Actor(group, (255, 0, 255),   1, (110, 110))#Magenta
# Actor(group, (0, 255, 255),   0, (120, 120))#Cyan
# Actor(group, (255, 255, 0),   3, (130, 130))#Yellow
# Actor(group, (0, 0, 255),     2, (140, 140))#Blue

# run = True
# while run:
#     for e in pygame.event.get():
#         if e.type ==pygame.QUIT:
#             run = False
#     screen.fill((0,0,0))
#     x = pygame.mouse.get_pos()[0]
#     y = pygame.mouse.get_pos()[1]
#     group.draw(screen)
#     pygame.draw.circle(screen, (0, 0, 255), (x, y), 25)
#     group.update()
#     pygame.display.flip()


#//////////////Transparency
# import pygame
# pygame.init()

# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255, 50)  # This color contains an extra integer. It's the alpha value.
# PURPLE = (255, 0, 255)

# screen = pygame.display.set_mode((200, 325))
# screen.fill(WHITE)  # Make the background white. Remember that the screen is a Surface!
# clock = pygame.time.Clock()

# size = (50, 50)
# red_image = pygame.Surface(size)
# green_image = pygame.Surface(size)
# blue_image = pygame.Surface(size, pygame.SRCALPHA)  # Contains a flag telling pygame that the Surface is per-pixel alpha
# purple_image = pygame.Surface(size)

# red_image.set_colorkey(BLACK)
# green_image.set_alpha(50)
# # For the 'blue_image' it's the alpha value of the color that's been drawn to each pixel that determines transparency.
# purple_image.set_colorkey(BLACK)
# purple_image.set_alpha(50)

# pygame.draw.rect(red_image, RED, red_image.get_rect(), 10)
# pygame.draw.rect(green_image, GREEN, green_image.get_rect(), 10)
# pygame.draw.rect(blue_image, BLUE, blue_image.get_rect(), 10)
# pygame.draw.rect(purple_image, PURPLE, purple_image.get_rect(), 10)

# while True:
#     clock.tick(60)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             quit()
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_1:
#                 screen.blit(red_image, (75, 25))
#             elif event.key == pygame.K_2:
#                 screen.blit(green_image, (75, 100))
#             elif event.key == pygame.K_3:
#                 screen.blit(blue_image, (75, 175))
#             elif event.key == pygame.K_4:
#                 screen.blit(purple_image, (75, 250))

#     pygame.display.update()

# #//////Cicle mouvementimport pygame
# import sys
# import pygame
# SCREEN_SIZE = WIDTH, HEIGHT = (640, 480)
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# RED = (255, 50, 50)
# GREEN = (50, 255, 50)
# CIRCLE_RADIUS = 30

# # Initialization
# pygame.init()
# screen = pygame.display.set_mode(SCREEN_SIZE)
# pygame.display.set_caption('Circles')
# fps = pygame.time.Clock()
# paused = False

# # Ball setup
# ball_pos1 = [50, 0]
# ball_pos2 = [240, 0]
# ball_pos3 = [430, 0]

# def update():
#     ball_pos1[1] += 5
#     ball_pos2[1] += 3
#     ball_pos3[1] += 1


# def render():
#     screen.fill(BLACK)
#     pygame.draw.circle(screen, RED, ball_pos1, CIRCLE_RADIUS, 0)
#     pygame.draw.circle(screen, WHITE, ball_pos2, CIRCLE_RADIUS, 0)
#     pygame.draw.circle(screen, GREEN, ball_pos3, CIRCLE_RADIUS, 0)
#     pygame.display.update()
#     fps.tick(60)
# def collision():
#     x,y = pygame.mouse.get_pos()
#     bax  = ball_pos3[0]
#     bay  = ball_pos3[1]
#     # print(list(pygame.mouse.get_pos()),ball_pos3 )
#     # pygame.time.delay(1000)
#     if(x<bax+CIRCLE_RADIUS and x>bax-CIRCLE_RADIUS ):
#         # print("in x zone")
#         if(y<bay+CIRCLE_RADIUS and y>bay-CIRCLE_RADIUS):
#             # print("in y zone")
#             return True
#     else:
#         return False
# def cache():
#     pygame.draw.circle(screen, (255,0,0), (100,200), CIRCLE_RADIUS, 0)

# while True:
#     # x,y = pygame.mouse.get_pos()
#     # bax  = ball_pos3[0]
#     # bay  = ball_pos3[1]
#     # print(list(pygame.mouse.get_pos()),ball_pos3 )
#     # # pygame.time.delay(1000)
#     # if(x<bax+CIRCLE_RADIUS and x>bax-CIRCLE_RADIUS ):
#     #     print("in x zone")
#     #     if(y<bay+CIRCLE_RADIUS and y>bay-CIRCLE_RADIUS):
#     #         print("in y zone")
#             # pygame.draw.circle(screen, (0,0,0), ball_pos3, CIRCLE_RADIUS, 0)
#             # cache()
#     if(list() == ball_pos3):
#         print("collision")
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         if event.type == pygame.KEYUP:
#             if event.key == pygame.K_SPACE:
#                 paused = not paused
#     if not paused:
#         update()
#         render()
#         if collision():
#             cache()
#             pygame.time.delay(1000)

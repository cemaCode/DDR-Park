from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import cv2
import sys

camera = cv2.VideoCapture(0)
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
screen = pygame.display.set_mode([1000,600])
w, h = pygame.display.get_surface().get_size()
camera.set(3, h)
camera.set(4, w)

try:
    while True:
        screen.fill([255, 255, 255])
        ret, frame = camera.read()

        # H, L = frame.shape[:2]
        # print(H,L)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame.swapaxes(0, 1)
        # cv2.flip(frame,0)
        # print(screen.get_size())
        # print(len(frame))
        # print(frame.get(3), frame.get(4))
        pygame.surfarray.blit_array(screen, frame)
        # pygame.display.update()
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]

        pygame.draw.circle(screen, (0, 0, 255), (x, y), 75)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    sys.exit(0)

except (KeyboardInterrupt, SystemExit):
    pygame.quit()
    cv2.destroyAllWindows()
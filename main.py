import pygame
import pygame.gfxdraw
import pygame.constants
import pygame.locals
import sys
from colors import *
import math

size = W, H = 1400, 800
FPS = 30

pygame.init()
display = pygame.display.set_mode(size)
clock = pygame.time.Clock()
screen = pygame.Surface(size)
radius = 150
# NOTE: Angle is in radians
angle = 0
# Angular speed along the largest circle
angular_speed = 0.000001
step_size = 0.001
center = 400, 400
wave = []
revolution_in_radians = 2 * 3.14

# Width of the rectangle having the sinusoidal graph
rect_width = 450
rect_offset = center[0] + 500

n = 0

while 1:
    display.blit(screen, (0, 0))
    pygame.display.flip()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                n += 1
            if event.key == pygame.K_s:
                n -= 1
            if event.key == pygame.K_q:
                step_size *= 0.01
            if event.key == pygame.K_e:
                step_size *= 10
                
    if pygame.key.get_pressed()[pygame.K_UP]:
        n += 1
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        n -= 1
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        angular_speed += step_size
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        angular_speed -= step_size
    
    font = pygame.font.SysFont('bahnschrift', 35)
    separator = ' '*25
    text = font.render(
            f"N:{n} {separator} Step Size: {round(step_size, 10)} {separator} Angular Speed: {round(angular_speed, 10)}", 
            True, 
            white
        )

    screen.fill(black)
    screen.blit(text, (20, 20))

    x, y = center
    for i in range(1, 2*n + 1, 2):
        prevx, prevy = x, y
        x += (radius / i) * math.cos(angle * i)
        y += (radius / i) * math.sin(angle * i)
        
        # pygame.draw.circle(screen, white, (prevx, prevy), radius /n, 2)
        pygame.gfxdraw.aacircle(screen, int(prevx), int(prevy), radius//i, white)
        # angle %= revolution_in_radians
        pygame.draw.circle(screen, red, (x, y), 1.5)
        pygame.draw.aaline(screen, yellow, (prevx, prevy), (x, y))
    
    angle += angular_speed
    wave.insert(0, y)
    pygame.draw.aaline(screen, medium_violet_red, (x, y), (rect_offset, wave[0]))
    
    if len(wave) > rect_width: wave.pop()
        
    pygame.draw.rect(screen, midnight_blue, pygame.Rect(rect_offset, center[1] - radius, rect_width, 2*radius))

    point_arr = [(rect_offset + i, w) for i, w in enumerate(wave)]
    if len(point_arr) > 2:
        pygame.draw.aalines(screen, yellow, False, point_arr, 2)
import pygame
import numpy as np

width, height = 64, 64
scale = 8
s_width, s_height = scale*width, scale*height
mx1, my1 = -1, -1
mx2, my2 = 1, 1
zoom = 1
speed = 0.1

pygame.init()
screen = pygame.display.set_mode((s_width,s_height))

running = True

iter_num = 30

frame = 0

while running:
    frame += 1
    print(frame)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        mx1 -= speed / zoom
        mx2 -= speed / zoom
    if keys[pygame.K_d]:
        mx1 += speed / zoom
        mx2 += speed / zoom
    if keys[pygame.K_w]:
        my1 -= speed / zoom
        my2 -= speed / zoom
    if keys[pygame.K_s]:
        my1 += speed / zoom
        my2 += speed / zoom
    if keys[pygame.K_q]:  # zoom out
        mx1 = mx1 + (mx2 - mx1) * - speed
        mx2 = mx2 + (mx1 - mx2) * - speed
        my1 = my1 + (my2 - my1) * - speed
        my2 = my2 + (my1 - my2) * - speed
        zoom /= (1 + speed) ** 2
    if keys[pygame.K_e]:  # zoom in
        mx1 = mx1 + (mx2 - mx1) * speed
        mx2 = mx2 + (mx1 - mx2) * speed
        my1 = my1 + (my2 - my1) * speed
        my2 = my2 + (my1 - my2) * speed
        zoom *= (1 + speed) ** 2

    img = pygame.Surface((width, height))
    
    for y in range(height):
        for x in range(width):
            sx = (x / width) * (mx2 - mx1) + mx1
            sy = (y / height) * (my2 - my1) + my1
            c = complex(sx, sy)
            z = 0
            for i in range(iter_num):
                z = z*z + c
                if abs(z) > 2:
                    color = int(255 * (i / iter_num))
                    img.set_at((x, y), (color,color,color))
                    break
            if i == iter_num - 1:
                img.set_at((x, y), (255,255,255))

    img = pygame.transform.scale(img, (s_width, s_height))    
    screen.blit(img, (0, 0))
    
    pygame.display.update()            

exit()

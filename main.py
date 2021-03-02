import pygame
import time

width, height = 64, 64  # RESOLUTION OF FRACTAL BEFORE SCALING
scale = 8
s_width, s_height = scale*width, scale*height  # SCREEN SIZE

speed = 0.1  # Zoom / movement speed

mx1, my1 = -1, -1
mx2, my2 = 1, 1
zoom = 1
mouse_x, mouse_y = 0, 0

pygame.init()
screen = pygame.display.set_mode((s_width,s_height))

running = True

iter_num = 30

frame = 0

while running:
    frame += 1
    #print(frame)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Movement/zoom stuffs
    mouse_x, mouse_y  = pygame.mouse.get_pos()
    mouse_left, _, mouse_right = pygame.mouse.get_pressed(num_buttons=3)
    tx, ty = mouse_x / s_width, mouse_y / s_height
    fx, fy = mx1 + (mx2 - mx1) * tx, my1 + (my2 - my1) * ty
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        width -= 1
        height -= 1
    if keys[pygame.K_d]:
        width += 1
        height += 1
    if width < 2:
        width = 2
    if height < 2:
        height = 2


    if keys[pygame.K_w]:
        iter_num += 1
    if keys[pygame.K_s]:
        iter_num -= 1
    
    if iter_num < 1:
        iter_num = 1

    if keys[pygame.K_q] or mouse_right:  # zoom out
        mx1 = mx1 + (fx - mx1) * -speed
        mx2 = mx2 + (fx - mx2) * -speed
        my1 = my1 + (fy - my1) * -speed
        my2 = my2 + (fy - my2) * -speed
        zoom /= (1 + speed) ** 2
    if keys[pygame.K_e] or mouse_left:  # zoom in
        mx1 = mx1 + (fx - mx1) * speed
        mx2 = mx2 + (fx - mx2) * speed
        my1 = my1 + (fy - my1) * speed
        my2 = my2 + (fy - my2) * speed
        zoom *= (1 + speed) ** 2


    # The juicy stuff
    img = pygame.Surface((width, height))
    for py in range(height):
        for px in range(width):
            x0 = (px / width) * (mx2 - mx1) + mx1
            y0 = (py / height) * (my2 - my1) + my1
            x = 0
            y = 0
            iters = 0

            x2 = 0
            y2 = 0
            while (x2 + y2 <= 4 and iters < iter_num):
                y = 2 * x * y + y0
                x = x2 - y2 + x0
                x2 = x * x
                y2 = y * y
                iters += 1

            color = 255 - int(255 * (iters / iter_num))
            img.set_at((px, py), (color,color,color))

    # Scale and blit
    img = pygame.transform.scale(img, (s_width, s_height)) 
    screen.blit(img, (0, 0))
    pygame.display.update()            

exit()

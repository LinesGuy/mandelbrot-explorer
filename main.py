import pygame
import time

width, height = 200, 200  # RESOLUTION OF FRACTAL BEFORE SCALING
scale = 2
s_width, s_height = scale*width, scale*height  # SCREEN SIZE

speed = 0.1  # Zoom / movement speed

mx1, mx2 = -1.5, 1.5
my1, my2 = -1.5, 1.5
zoom = 1
mouse_x, mouse_y = 0, 0

power = 2

pygame.init()
screen = pygame.display.set_mode((s_width,s_height))

running = True

iter_num = 5

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
    fx = mx1 + (mx2 - mx1) * (mouse_x / s_width)
    fy = my1 + (my2 - my1) * (mouse_y / s_height)
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
    
    if keys[pygame.K_q]:
        power -= 0.05
    if keys[pygame.K_e]:
        power += 0.05
    
    print("power =", power)

    if mouse_right:  # zoom out
        mx1 = mx1 + (fx - mx1) * -speed
        mx2 = mx2 + (fx - mx2) * -speed
        my1 = my1 + (fy - my1) * -speed
        my2 = my2 + (fy - my2) * -speed
        zoom /= (1 + speed) ** 2
    if mouse_left:  # zoom in
        mx1 = mx1 + (fx - mx1) * speed
        mx2 = mx2 + (fx - mx2) * speed
        my1 = my1 + (fy - my1) * speed
        my2 = my2 + (fy - my2) * speed
        zoom *= (1 + speed) ** 2


    # The juicy stuff
    img = pygame.Surface((width, height))
    for y in range(height):
        for x in range(width):
            sx = (x / width) * (mx2 - mx1) + mx1
            sy = (y / height) * (my2 - my1) + my1
            c = complex(sx, sy)
            z = complex(0, 0)
            for i in range(iter_num):
                z = z ** power + c  #  z^2 + c
                if abs(z) > 2:  # If distance from origin > 2 then diverged
                    # Diverged, colour based on iterations
                    color = 255 - int(255 * (i / iter_num) * 0.5)
                    img.set_at((x, y), (color,color,color))
                    break
            if i == iter_num - 1:
                # ^ if still converged after iter_num many iterations,
                # make pixel black
                img.set_at((x, y), (0, 0, 0))

    # Scale and blit
    img = pygame.transform.scale(img, (s_width, s_height)) 
    screen.blit(img, (0, 0))
    pygame.display.update()            

exit()

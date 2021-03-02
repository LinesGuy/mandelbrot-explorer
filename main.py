import pygame

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

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Movement/zoom stuffs
    mouse_x, mouse_y  = pygame.mouse.get_pos()
    tx, ty = mouse_x / s_width, mouse_y / s_height
    fx, fy = mx1 + (mx2 - mx1) * tx, my1 + (my2 - my1) * ty
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        width -= 1
        height -= 1
    if keys[pygame.K_d]:
        width += 1
        height += 1

    if keys[pygame.K_w]:
        iter_num += 1
    if keys[pygame.K_s]:
        iter_num -= 1

    if keys[pygame.K_q]:  # zoom out
        mx1 = mx1 + (fx - mx1) * -speed
        mx2 = mx2 + (fx - mx2) * -speed
        my1 = my1 + (fy - my1) * -speed
        my2 = my2 + (fy - my2) * -speed
        zoom /= (1 + speed) ** 2
    if keys[pygame.K_e]:  # zoom in
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
            for i in range(iter_num):  # Iterate loop
                z = z*z + c  #  z^2 + c
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

import pygame
background_image_filename = 'sushiplate.jpg'
pygame.init()
screen = pygame.display.set_mode([900,700])
screen.fill([255,255,255])
pygame.display.set_caption("game test")
background = pygame.image.load(background_image_filename).convert()
screen.blit(background, (0,0))
pygame.draw.circle(screen,[255,0,0],[800,100],60,0) #颜色、坐标、半径、是否填充
pygame.display.flip()
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

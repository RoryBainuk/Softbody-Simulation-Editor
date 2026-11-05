import pygame

pygame.init() #initialise the pygame library
screen = pygame.display.set_mode((600,600), pygame.RESIZABLE) #create a pygame screen that is resizable
pygame.display.set_caption("Simulation Enviroment")
clock = pygame.time.Clock() #create a clock for controlling fps
running = True


#MAIN LOOP
while running:
    clock.tick(60)

    #fill screen with background colour
    screen.fill((50,50,50)) 

    #checking for quiting of application
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    pygame.display.update() #update screen

pygame.quit()

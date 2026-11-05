def Run():
    import pygame 
    import UI_Elements
    import Sims
    import sys
    import tkinter as tk
    import os
    root = tk.Tk()

    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (root.winfo_screenwidth()//2 - 400, root.winfo_screenheight()//2 - 400)

    screen = pygame.display.set_mode((800,800)) #create a pygame screen
    pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock() #create a clock for controlling fps
    running = True

    #Create Title Text
    TitleFont = pygame.font.SysFont("Arial", 100, True)
    title = TitleFont.render("Spring Sim", True, (0,0,0))

    #Create Buttons
    quitButton = UI_Elements.Button(pygame.Vector2(400,625), "Quit", (255,0,0), 50)
    ClothButton = UI_Elements.Button(pygame.Vector2(400,425), "Cloth Sim", (100,100,200), 50)
    SoftButton = UI_Elements.Button(pygame.Vector2(400,525), "Sofy Body Sim", (100,200,100), 50)
    PendulumButton = UI_Elements.Button(pygame.Vector2(400, 325), "Pendulum Sim", (100,200,200), 50)


    #MAIN LOOP
    while running:
        clock.tick(60)

        #fill screen with background colour
        screen.fill((150,150,150)) 

        #Draw all the text and buttons
        screen.blit(title, (400 - (title.get_width()/2), 100))
        quitButton.Draw(screen)
        ClothButton.Draw(screen)
        SoftButton.Draw(screen)
        PendulumButton.Draw(screen)

        #Switch to the Cloth Sim
        if ClothButton.OnClick():
            pygame.quit()
            Sims.Cloth()
            sys.exit()

        #Switch to the Soft Body Sim
        if SoftButton.OnClick():
            pygame.quit()
            Sims.SoftBody()
            sys.exit()

        #Switch to the Pendulum Sim
        if PendulumButton.OnClick():
            pygame.quit()
            Sims.Pendulum()
            sys.exit()

        

        #Quit the application
        if quitButton.OnClick():
            running = False

        #checking for quiting of application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        pygame.display.update() #update screen

    pygame.quit()


if __name__ == "__main__":
    Run()

    
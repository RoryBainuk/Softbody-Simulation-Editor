import pygame
from multiprocessing import Process, Queue, set_start_method
import os
import Cloth_Simulation_Env
import SoftBody_Simulation_Env
import Pendulum_Simulation_Env
from UI_Elements import Slider, Button, Textbox
import tkinter as tk
import Main_Menu
import sys
root = tk.Tk()

def ClothParametersPanel(kQ,widthQ,heightQ,springLengthQ,PointSizeQ, ResetQ, StrengthQ):
    #Sender Window: sends messages to Window B
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (root.winfo_screenwidth()*0.7,30)

    pygame.init()
    screen = pygame.display.set_mode((400, 800))
    pygame.display.set_caption("Cloth Parameters")

    font = pygame.font.SysFont("Arial", 20)
    #reset button
    reset = Button(pygame.Vector2(100, 450), "Reset", (200, 100, 100), 30,textColour=(255,255,255))
    quit = Button(pygame.Vector2(200, 450), "Quit", (255, 0, 0), 30,textColour=(255,255,255))

    #spring constant slider
    kText = font.render("Spring Constant", True, (0,0,0))
    KSlider = Slider(10, 200, 90, 300, 30, pygame.Vector2(200, 100))

    #spring length slider
    lengthText = font.render("Spring Length", True, (0,0,0))
    lengthSlider = Slider(10, 30, 20, 300, 30, pygame.Vector2(200, 650))

    #strength slider
    tearText = font.render("Strength", True, (0,0,0))
    tearSlider = Slider(150, 350, 275, 300, 30, pygame.Vector2(200, 200))

    #point size slider
    PointText = font.render("PointSize", True, (0,0,0))
    PointSlider = Slider(0, 15, 5, 300, 30, pygame.Vector2(200, 300))

    #cloth width TextBox
    WidthText = font.render("Width", True, (0,0,0))
    widthBox = Textbox(40, 35, pygame.Vector2(70, 550), maxCharacters = 2, NumsOnly=True)
    widthBox.SetText("20")

    #cloth height TextBox
    HeightText = font.render("Height", True, (0,0,0))
    HeightBox = Textbox(40, 35, pygame.Vector2(200, 550), maxCharacters = 2, NumsOnly=True)
    HeightBox.SetText("20")

    clock = pygame.time.Clock()
    running = True

    #set intial values
    k = KSlider.GetValue()
    length = lengthSlider.GetValue()
    width = widthBox.GetText()
    height = HeightBox.GetText()
    strength = tearSlider.GetValue()
    size = PointSlider.GetValue()

    # the windows main loop
    while running:
        clock.tick(60)  
        screen.fill((200,200,200))
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        #Quit Sim
        quit.Draw(screen)
        if quit.OnClick():
            ResetQ.put(False)
            pygame.quit()
            Main_Menu.Run()
            sys.exit()

        #reset Sim
        reset.Draw(screen)
        if reset.OnClick():
            #enqueue data
            ResetQ.put(True)

        #Spring constant slider
        screen.blit(kText, (50, 55))
        KSlider.Draw(screen)
        KSlider.Update(events)
        if KSlider.GetValue() != k:
            #enqueue data
            kQ.put(KSlider.GetValue()/10000)
        k = KSlider.GetValue()

        #Spring Length slider
        screen.blit(lengthText, (50, 605))
        lengthSlider.Draw(screen)
        lengthSlider.Update(events)
        if lengthSlider.GetValue() != length:
            #enqueue data
            springLengthQ.put(lengthSlider.GetValue())
        length = lengthSlider.GetValue()

        #Strength slider
        screen.blit(tearText, (50, 155))
        tearSlider.Draw(screen)
        tearSlider.Update(events)
        if tearSlider.GetValue() != strength:
            #enqueue data
            StrengthQ.put(tearSlider.GetValue()/100)
        strength = tearSlider.GetValue()

        #Point slider
        screen.blit(PointText, (50, 255))
        PointSlider.Draw(screen)
        PointSlider.Update(events)
        if PointSlider.GetValue() != size:
            #enqueue data
            PointSizeQ.put(PointSlider.GetValue())
        size = PointSlider.GetValue()

        #Width TextBox
        screen.blit(WidthText, (50, 505))
        widthBox.Draw(screen)
        widthBox.Update(events)
        if widthBox.GetText() != width and widthBox.GetText() != "":
            #enqueue data
            widthQ.put(int(widthBox.GetText()))
        width = widthBox.GetText()


        #Height TextBox
        screen.blit(HeightText, (180, 505))
        HeightBox.Draw(screen)
        HeightBox.Update(events)
        if HeightBox.GetText() != height and HeightBox.GetText() != "":
            #enqueue data
            heightQ.put(int(HeightBox.GetText()))
        height = HeightBox.GetText()
        

        pygame.display.flip()
    pygame.quit()

def ClothSimEnv(k,width,height,springLength,PointSize, resetQ, StrengthQ):
    Cloth_Simulation_Env.ClothWindow(k,width,height,springLength,PointSize, resetQ, StrengthQ)



def SoftBodyParametersPanel(kQ, ResetQ, gravityQ, radQ, resQ, stifQ):
    #Sender Window: sends messages to Window B
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (root.winfo_screenwidth()*0.7,30)

    pygame.init()
    screen = pygame.display.set_mode((400, 800))
    pygame.display.set_caption("Soft Body Parameters")

    font = pygame.font.SysFont("Arial", 20)
    #reset button
    reset = Button(pygame.Vector2(100, 450), "Reset", (200, 100, 100), 30,textColour=(255,255,255))
    quit = Button(pygame.Vector2(200, 450), "Quit", (255, 0, 0), 30,textColour=(255,255,255))

    #spring constant slider
    kText = font.render("Spring Constant", True, (0,0,0))
    KSlider = Slider(20, 500, 200, 300, 30, pygame.Vector2(200, 100))

    #stiffness slider
    stifText = font.render("Stiffness", True, (0,0,0))
    stiffSlider = Slider(1, 15, 6, 300, 30, pygame.Vector2(200, 200))

    #radius slider
    radiusText = font.render("Radius", True, (0,0,0))
    radiusSlider = Slider(10, 200, 50, 300, 30, pygame.Vector2(200, 650))

    #Gravity slider
    gravityText = font.render("Gravity", True, (0,0,0))
    gravitySlider = Slider(0, 150, 50, 300, 30, pygame.Vector2(200, 300))

    #resolution slider
    resText = font.render("Sides", True, (0,0,0))
    resSlider = Slider(3, 30, 20, 300, 30, pygame.Vector2(200, 550))

    clock = pygame.time.Clock()
    running = True

    #set intial values
    k = KSlider.GetValue()
    radius = radiusSlider.GetValue()
    gravity = gravitySlider.GetValue()
    resolution = resSlider.GetValue()
    stiffness = stiffSlider.GetValue()

    # the windows main loop
    while running:
        clock.tick(60)  
        screen.fill((200,200,200))
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        #Quit Sim
        quit.Draw(screen)
        if quit.OnClick():
            ResetQ.put(False)
            pygame.quit()
            Main_Menu.Run()
            sys.exit()

        #reset Sim
        reset.Draw(screen)
        if reset.OnClick():
            #enqueue data
            ResetQ.put(True)

        #Spring constant slider
        screen.blit(kText, (50, 55))
        KSlider.Draw(screen)
        KSlider.Update(events)
        if KSlider.GetValue() != k:
            #enqueue data
            kQ.put(KSlider.GetValue())
        k = KSlider.GetValue()

        #Stiffness slider
        screen.blit(stifText, (50, 155))
        stiffSlider.Draw(screen)
        stiffSlider.Update(events)
        if stiffSlider.GetValue() != stiffness:
            #enqueue data
            stifQ.put(stiffSlider.GetValue())
        stiffness = stiffSlider.GetValue()

        #radius slider
        screen.blit(radiusText, (50, 605))
        radiusSlider.Draw(screen)
        radiusSlider.Update(events)
        if radiusSlider.GetValue() != radius:
            #enqueue data
            radQ.put(radiusSlider.GetValue())
        radius  = radiusSlider.GetValue()

        #gravity slider
        screen.blit(gravityText, (50, 255))
        gravitySlider.Draw(screen)
        gravitySlider.Update(events)
        if gravitySlider.GetValue() != gravity:
            #enqueue data
            gravityQ.put(gravitySlider.GetValue()/100)
        gravity = gravitySlider.GetValue()

        #resolution slider
        screen.blit(resText, (50, 505))
        resSlider.Draw(screen)
        resSlider.Update(events)
        if resSlider.GetValue() != resolution:
            #enqueue data
            resQ.put(resSlider.GetValue())
        resolution = resSlider.GetValue()

        pygame.display.flip()
    pygame.quit()

def SoftBodySimEnv(kQ, resetQ, gravityQ, radQ, resQ, stifQ):
    SoftBody_Simulation_Env.Run(kQ, resetQ, gravityQ, radQ, resQ, stifQ)



def PendulumParametersPanel(kQ, ResetQ, angleQ, dampQ, lenQ, numQ, PlayQ):
    #Sender Window: sends messages to Window B
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (root.winfo_screenwidth()*0.7,30)

    pygame.init()
    screen = pygame.display.set_mode((400, 800))
    pygame.display.set_caption("Pendulum Parameters")



    font = pygame.font.SysFont("Arial", 20)
    #reset button
    reset = Button(pygame.Vector2(100, 450), "Reset", (200, 100, 100), 30, textColour=(255,255,255))
    play = Button(pygame.Vector2(250, 450), "Play/Pause", (100, 100, 200), 30,textColour=(255,255,255))
    quit = Button(pygame.Vector2(87, 400), "Quit", (255, 0, 0), 30, textColour=(255,255,255))

    #spring constant slider
    kText = font.render("Spring Constant", True, (0,0,0))
    KSlider = Slider(1, 15, 7, 300, 30, pygame.Vector2(200, 100))

    #Length slider
    lengthText = font.render("Spring Length", True, (0,0,0))
    lengthSlider = Slider(20, 500, 200, 300, 30, pygame.Vector2(200, 200))

    #num TextBox
    numText = font.render("Points", True, (0,0,0))
    numBox = Textbox(40, 35, pygame.Vector2(70, 550), maxCharacters = 2, NumsOnly=True)
    numBox.SetText("1")

    #Damping
    dampingText = font.render("Damping", True, (0,0,0))
    dampingSlider = Slider(0, 100, 0, 300, 30, pygame.Vector2(200, 300))

    #Angle slider
    angleText = font.render("Angle", True, (0,0,0))
    angleSlider = Slider(0, 90, 45, 300, 30, pygame.Vector2(200, 650))

    clock = pygame.time.Clock()
    running = True

    #set intial values
    k = KSlider.GetValue()
    length = lengthSlider.GetValue()
    num = numBox.GetText()
    damping = dampingSlider.GetValue()
    angle = angleSlider.GetValue()

    # the windows main loop
    while running:
        clock.tick(60)  
        screen.fill((200,200,200))
        events = pygame.event.get()

        #search for keyboard events
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        #Quit Sim
        quit.Draw(screen)
        if quit.OnClick():
            ResetQ.put(False)
            pygame.quit()
            Main_Menu.Run()
            sys.exit()

        #reset Sim
        reset.Draw(screen)
        if reset.OnClick():
            #enqueue data
            ResetQ.put(True)


        play.Draw(screen)
        if play.OnClick():
            #enqueue data
            PlayQ.put(True)

        #Spring constant slider
        screen.blit(kText, (50, 55))
        KSlider.Draw(screen)
        KSlider.Update(events)
        if KSlider.GetValue() != k:
            #enqueue data
            kQ.put(KSlider.GetValue()/10000)
        k = KSlider.GetValue()

        #Length Slider
        screen.blit(lengthText, (50, 155))
        lengthSlider.Draw(screen)
        lengthSlider.Update(events)
        if lengthSlider.GetValue() != length:
            #enqueue data
            lenQ.put(lengthSlider.GetValue())
        length = lengthSlider.GetValue()

        #Damping Slider
        screen.blit(dampingText, (50, 255))
        dampingSlider.Draw(screen)
        dampingSlider.Update(events)
        if dampingSlider.GetValue() != damping:
            realValue = dampingSlider.upper - dampingSlider.GetValue()
            #enqueue data
            if realValue != 100:
                dampQ.put(0.99 + (realValue/10000))
            else:
                dampQ.put(1)
        damping = dampingSlider.GetValue()

        #Angle Slider
        screen.blit(angleText, (50, 605))
        angleSlider.Draw(screen)
        angleSlider.Update(events)
        if angleSlider.GetValue() != angle:
            #enqueue data
            angleQ.put(angleSlider.GetValue())
        angle = angleSlider.GetValue()


        #Num TextBox
        screen.blit(numText, (50, 505))
        numBox.Draw(screen)
        numBox.Update(events)
        if numBox.GetText() != num and numBox.GetText() != "":
            #enqueue data
            numQ.put(int(numBox.GetText()))
        num = numBox.GetText()

        pygame.display.flip()
    pygame.quit()

def PendulumSimEnv(kQ, ResetQ, angleQ, dampQ, lenQ, numQ, PlayQ):
    Pendulum_Simulation_Env.Run(kQ, ResetQ, angleQ, dampQ, lenQ, numQ, PlayQ)


#Cloth Sim
def Cloth():
    try:
        set_start_method("spawn")  # Required on Windows
    except RuntimeError:
        pass
    #create queue
    k = Queue()
    width = Queue()
    height = Queue()
    springLength = Queue()
    PointSize = Queue()
    ResetQ = Queue()
    StrengthQ = Queue()

    #create processes for each core using the procedures
    p1 = Process(target=ClothParametersPanel, args=(k,width,height,springLength,PointSize, ResetQ, StrengthQ,))
    p2 = Process(target=ClothSimEnv, args=(k,width,height,springLength,PointSize, ResetQ, StrengthQ,))

    #run the processes
    p1.start()
    p2.start()

    #waiting for the processes to finish
    p1.join()
    p2.join()


#Soft Body Sim
def SoftBody():
    try:
        set_start_method("spawn")  # Required on Windows
    except RuntimeError:
        pass
    #create queue
    kQ = Queue()
    resetQ = Queue()
    gravityQ = Queue()
    radQ = Queue()
    resQ = Queue()
    stifQ = Queue()

    #create processes for each core using the procedures
    p1 = Process(target=SoftBodyParametersPanel, args=(kQ, resetQ, gravityQ, radQ, resQ, stifQ, ))
    p2 = Process(target=SoftBodySimEnv, args=(kQ, resetQ, gravityQ, radQ, resQ, stifQ, ))

    #run the processes
    p1.start()
    p2.start()

    #waiting for the processes to finish
    p1.join()
    p2.join()


#Pendulum Sim
def Pendulum():
    try:
        set_start_method("spawn")  # Required on Windows
    except RuntimeError:
        pass
    #create queue
    kQ = Queue()
    ResetQ = Queue()
    angleQ = Queue()
    dampQ = Queue()
    lenQ = Queue()
    numQ = Queue()
    PlayQ = Queue()

    #create processes for each core using the procedures
    p1 = Process(target=PendulumParametersPanel, args=(kQ, ResetQ, angleQ, dampQ, lenQ, numQ, PlayQ,))
    p2 = Process(target=PendulumSimEnv, args=(kQ, ResetQ, angleQ, dampQ, lenQ, numQ, PlayQ,))

    #run the processes
    p1.start()
    p2.start()

    #waiting for the processes to finish
    p1.join()
    p2.join()


if __name__ == "__main__":
    Pendulum()

    
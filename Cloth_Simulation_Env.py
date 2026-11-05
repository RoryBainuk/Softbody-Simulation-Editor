import pygame
import Point
import Spring
import SBShape
import math
import os
import tkinter as tk
root = tk.Tk()

def ClothWindow(kQ,widthQ,heightQ,springLengthQ,PointSizeQ, resetQ, StrengthQ):

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (root.winfo_screenwidth()*0.15, 30)

    pygame.init() #initialise the pygame library
    screen = pygame.display.set_mode((600,600), pygame.RESIZABLE) #create a pygame screen that is resizable
    pygame.display.set_caption("Cloth Simulation Enviroment")
    clock = pygame.time.Clock() #create a clock for controlling fps
    running = True

    def CreateCloth(width, height, restLength):
        particles = []
        springs = []

        clothWidth = (width * restLength)/2
        middle = screen.get_width()/2 - clothWidth

        #Creating each point
        for i in range(0, width):
            particles.append([])
            for j in range(0,height):
                #Checking for top row to enable gravity
                if j != 0:
                    particles[i].append(Point.ClothPoint(pygame.Vector2((i * restLength)+ middle, (j * restLength)),
                                                    pygame.Vector2(0,0), PointSize))
                else:
                    particles[i].append(Point.ClothPoint(pygame.Vector2((i * restLength)+middle, (j * restLength)),
                                                    pygame.Vector2(0,0), PointSize, True))

        #looping through every point
        for i in range(0, len(particles)):
            for j in range(0, len(particles[i])):
                #Checking For Edge
                if j != 0:
                    a = particles[i][j]
                    b = particles[i][j - 1]
                    springs.append(Spring.ClothSpring(restLength, a, b))
                #Checking For Edge
                if i != 0:
                    a = particles[i][j]
                    b = particles[i-1][j]
                    springs.append(Spring.ClothSpring(restLength, a, b))
                #Checking For Edge
                if i != 0 and j != 0:
                    a = particles[i][j]
                    b = particles[i-1][j-1]
                    #Calculating the length of the springs
                    length = (restLength * restLength) + (restLength * restLength)
                    length = math.sqrt(length)
                    springs.append(Spring.ClothSpring(length, a, b))
                #Checking For Edge
                if i != 0 and j != len(particles[i])-1:
                    a = particles[i][j]
                    b = particles[i-1][j+1]
                    #Calculating the length of the springs
                    length = (restLength * restLength) + (restLength * restLength)
                    length = math.sqrt(length)
                    springs.append(Spring.ClothSpring(length, a, b))

        #set the spring constant to an appropriate value
        springs[0].SetSpringConstant(k)
        particles[0][0].SetGravityConstant(0.2)

        return particles, springs
    

    def Reset(width, height, length):
        verticies, springs = CreateCloth(width, height,length)
        #Create a cloth object
        cloth = SBShape.Cloth(verticies, springs)
        return cloth


    width = 20
    height = 20
    length = 20
    k = 0.009
    PointSize = 5
    #Create point and spring lists
    verticies, springs = CreateCloth(width, height,length)
    #Create a cloth object
    cloth = SBShape.Cloth(verticies, springs)

    winwidth = screen.get_width()


    #MAIN LOOP
    while running:
        clock.tick(60)

        #fill screen with background colour
        screen.fill((50,50,50)) 

        #update and draw cloth
        cloth.Update()
        cloth.Draw(screen)

        newWidth = screen.get_width()
        if newWidth != winwidth:
            widthDiff = (newWidth - winwidth) / 2
            for p in cloth.points:
                for j in p:
                    j.pos.x += widthDiff

        winwidth = screen.get_width()


        #check for right click pressed
        if pygame.mouse.get_pressed()[2]:
            #get mouse cursor coordinates
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
            #loop through all points in the cloth
            for i in cloth.points:
                for j in i:
                    #check if the point is within close enough range to the cursor
                    if abs(j.pos.x - mouseX) < 10 and abs(j.pos.y - mouseY) < 10:
                        #remove the point            
                        temp = j
                        i.remove(j)
                        
                        #loop through every spring and remove the point
                        for s in cloth.springs:
                            if s.a == temp:
                                s.a = None
                            if s.b == temp:
                                s.b = None
                        
        #check for left click
        if pygame.mouse.get_pressed()[0]:
            #get mouse coordinates
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
            mousePos = pygame.Vector2(mouseX, mouseY)

            #loop through every point in the cloth
            for i in cloth.points:
                for j in i:
                    offest = j.pos - mousePos
                    #check if the point is within close enough range to the cursor
                    if (offest).magnitude() <= 10:
                        #set its position to mouse coordinates
                        j.pos = mousePos
                        j.vel = pygame.Vector2(0,0)
                        j.accel = pygame.Vector2(0,0)

        #Update Parameters
        #reset Sim
        if not resetQ.empty():
            if resetQ.get() == True:
                cloth = Reset(width, height, length)
            else:
                running = False

        #Update spring length
        if not springLengthQ.empty():
            length = springLengthQ.get()
            cloth = Reset(width, height, length)

        #Update spring constant
        if not kQ.empty():
            k = kQ.get()
            cloth.springs[0].SetSpringConstant(k) 

        #Update cloth width
        if not widthQ.empty():
            width = widthQ.get()

        #Update cloth height
        if not heightQ.empty():
            height = heightQ.get()

        #Update spring strength
        if not StrengthQ.empty():
            cloth.SetTearConstant(StrengthQ.get())

        #change point size
        if not PointSizeQ.empty():
            newRad = PointSizeQ.get()
            for i in cloth.points:
                for j in i:
                    j.radius = newRad
            PointSize = newRad
            
        #checking for quiting of application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        pygame.display.update() #update screen

    pygame.quit()

    
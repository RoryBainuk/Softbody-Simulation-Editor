import pygame
import math
import Point
import Spring
import SBShape
import os
import tkinter as tk
root = tk.Tk()

#Create points in a circle for the soft Body
def CreateCirclePoints(center, radius, resolution):
    #create a lsit for the points
    pos = []
    step = 360/resolution

    #loops through for the number of points needed for the resolution
    for i in range(0, resolution):
        #Calculate the angle
        angle = step * i
        angle = math.radians(angle)
        #use trigonometry to calculate the x and y
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        position = pygame.Vector2(center.x + x, center.y + y)
        #Create a pointMass object at the positon
        point = Point.PointMass(position, pygame.Vector2(0,0), 5, False)
        pos.append(point)

    #return list of points
    return pos

def CreateCircleSprings(verticies):
    springs = []

    #Outer Springs
    #Loop Through All points
    for i in range(0, len(verticies)):
        #Check for last Point for special case.
        if i != len(verticies) - 1:
            #get the points for the spring
            a = verticies[i]
            b = verticies[i + 1]
            #Calculate Rest Length
            dif = (a.pos - b.pos)
            dist = dif.length()
            #Append List with a spring
            springs.append(Spring.Spring(dist, a, b, IsExternal=True))
        else:
            #get the points for the spring
            a = verticies[i]
            b = verticies[0]
            #Calculate Rest Length
            dif = (a.pos - b.pos)
            dist = dif.length()
            #Append List with a spring
            springs.append(Spring.Spring(dist, a, b, IsExternal=True))   

    #Internal Springs
    #loop thorugh every pair of points.
    for i in range(0, len(verticies)):
        for j in range(0, len(verticies)):
            if verticies[i] != verticies[j]:
                #check the points are not the same
                if abs(j - i) != 1 and abs(i-j) != len(verticies) - 1:
                    #get the points for the spring
                    a = verticies[i]
                    b = verticies[j]
                    #Calculate Rest Length
                    dif = (a.pos - b.pos)
                    dist = dif.length()
                    #Append List with a spring
                    springs.append(Spring.Spring(dist, a, b,(255,0,0), False))       

    #return Spring List
    return springs

def Reset(radius, resolution, k, gravity, screen):
    #create points and springs for the circle
    points = CreateCirclePoints(pygame.Vector2(screen.get_width()/2, screen.get_height()/2), radius, resolution)
    springs = CreateCircleSprings(points)
    #create the soft body object
    Ball = SBShape.SBShape(points, springs)
    Ball.springs[0].SetSpringConstant(k)
    Ball.points[0].SetGravityConstant(gravity)   
    return Ball


def Run(kQ, resetQ, gravityQ, radQ, resQ, stifQ):

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (root.winfo_screenwidth()*0.15, 30)

    pygame.init() #initialise the pygame library
    screen = pygame.display.set_mode((600,600), pygame.RESIZABLE) #create a pygame screen that is resizable
    pygame.display.set_caption("Soft Body Simulation Enviroment")
    clock = pygame.time.Clock() #create a clock for controlling fps
    running = True

    #create opaque surface
    surf = pygame.Surface((400,400))
    surf.set_colorkey((0,0,0))
    surf.set_alpha(50)
    #draw circle on the surface
    pygame.draw.circle(surf, (255,255,0), (200,200), 200)

    #create points and springs for the circle
    radius = 100
    resolution = 20
    k = 200
    gravity = 0.5
    stiffness = 20

    Ball = Reset(radius, resolution, k, gravity, screen)

    #MAIN LOOP
    while running:
        clock.tick(60)

        #fill screen with background colour
        screen.fill((50,50,50)) 

        #Update and draw the object
        Ball.Update(screen)
        Ball.Draw(screen)

        #Get left click
        if pygame.mouse.get_pressed()[0]:
            #get mosue position
            mousePos = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            averagePos = pygame.Vector2(0,0)
            #loop through all points in the object
            for i in Ball.points:
                #calculate force
                force = -0.005 * (i.pos - mousePos)
                #apply force
                i.vel += force
                #Calculate average position
                averagePos = averagePos + i.pos
            
            #Calculate average position of points
            averagePos = pygame.Vector2(averagePos.x / len(Ball.points), averagePos.y / len(Ball.points))
            pygame.draw.aaline(screen, "white", mousePos, averagePos) #Draw line to Mouse position


        #get right click
        if pygame.mouse.get_pressed()[2]:
            mousePos = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            for i in Ball.points:
                force = 0.01 * (i.pos - mousePos)
                if force.magnitude() <= 2:
                    i.vel += force
            
            #Draw transparent circle
            screen.blit(surf, mousePos - pygame.Vector2(200,200))

        #Reset Sim
        if not resetQ.empty():
            if resetQ.get() == True:
                Ball = Reset(radius, resolution, k, gravity, screen)
            else:
                running = False

        #Update radius
        if not radQ.empty():
            radius = radQ.get()
            Ball = Reset(radius, resolution, k, gravity, screen)

        #Update spring constant
        if not kQ.empty():
            k = kQ.get()
            Ball.springs[0].SetSpringConstant(k) 

        #Update stiffness
        if not stifQ.empty():
            stiffness = stifQ.get()
            Ball.springs[0].SetStiffness(stiffness) 

        #Update gravity
        if not gravityQ.empty():
            gravity = gravityQ.get()
            for i in Ball.points:
                i.accel = pygame.Vector2(0, gravity)
            Ball.points[0].SetGravityConstant(gravity)

        #Update resolution
        if not resQ.empty():
            resolution = resQ.get()
            Ball = Reset(radius, resolution, k, gravity, screen)

        #checking for quiting of application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        pygame.display.update() #update screen

    pygame.quit()


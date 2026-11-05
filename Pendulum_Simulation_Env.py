import pygame
import Point
import Spring
import math
import os
import tkinter as tk
root = tk.Tk()

def Run(kQ, ResetQ, angleQ, dampQ, lenQ, numQ, PlayQ):

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (root.winfo_screenwidth()*0.15, 30)

    pygame.init() #initialise the pygame library
    screen = pygame.display.set_mode((800,800), pygame.RESIZABLE) #create a pygame screen
    pygame.display.set_caption("Pendulum Simulation Enviroment")
    clock = pygame.time.Clock() #create a clock for controlling fps
    running = True
    
    def CreatePendulum(SpringLength, num, k, startingAngle, damping):
        anchor = Point.ClothPoint(pygame.Vector2(screen.get_width()/ 2, 0), pygame.Vector2(0,0), 5, True)

        #create spring and points list
        points = [anchor]
        springs = []

        #create points
        for i in range(0, num):
            #Calculate the position
            pos = pygame.Vector2((screen.get_width()/ 2) + ((SpringLength * (i+1)) * math.sin(math.radians(startingAngle))), 
                                (((SpringLength * (i+1)) * math.cos(math.radians(startingAngle)))))

            points.append(Point.ClothPoint(pos, pygame.Vector2(0,0), 5))

        #create springs
        for i in range(0, len(points)):
            if i != 0:
                springs.append(Spring.ClothSpring(SpringLength, points[i], points[i-1]))

        springs[0].SetSpringConstant(k)
        points[0].SetDamping(damping)

        return points, springs

    def Reset(springLength, num, k, startAngle, damping):
        points, springs = CreatePendulum(springLength, num, k, startAngle, damping)
        points[len(points)-1].vel = pygame.Vector2(0, 0)    
        return points, springs
    
    #variables
    k = 0.0007
    startAngle = 45
    damping = 1
    springLength = 200
    num = 1

    points, springs = CreatePendulum(springLength, num, k, startAngle, damping)

    width = screen.get_width()

    points[len(points)-1].vel = pygame.Vector2(0, 0)  
    pointVelocities = []  
    Play = True

    #MAIN LOOP
    while running:
        clock.tick(60)

        #fill screen with background colour
        screen.fill((50,50,50))   
            

        newWidth = screen.get_width()
        if newWidth != width:
            widthDiff = (newWidth - width) / 2
            for p in points:
                p.pos.x += widthDiff

        width = screen.get_width()

        for s in springs:
            if (s.a.pos - s.b.pos).magnitude() > 1000:
                springs.remove(s)


        #Store velocities
        if Play == False:
            #Store velocities
            if points[len(points)-1].vel != pygame.Vector2(0,0):
                pointVelocities = []       
                for i in points:
                    pointVelocities.append(i.vel)
                for i in points:
                    i.vel = pygame.Vector2(0,0)
        #Check if the sim is played
        elif Play == True:
            #If it was unpaused
            if pointVelocities != []:
                #Set velocities of points to the stored velocities.
                for i in range(0, len(pointVelocities)):
                    try:
                        points[i].vel = pointVelocities[i]
                    except IndexError:
                        pass
            #Update springs and points
            for i in springs:
                i.Update()
            for i in points:
                i.Update()

        #Draw springs and points
        for i in springs:
                i.Draw(screen)
        for i in points:
                i.Draw(screen)

        #check for left click
        if pygame.mouse.get_pressed()[0]:
            #get mouse coordinates
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
            #loop through every point in the cloth
            for i in points:
                #check if the point is within close enough range to the cursor
                if abs(i.pos.x - mouseX) <= 25 and abs(i.pos.y - mouseY) <= 25:
                    #set its position to mouse coordinates
                    i.pos.x = mouseX
                    i.pos.y = mouseY
                    i.vel = pygame.Vector2(0,0)
                    i.accel = pygame.Vector2(0,0)


        #Update Parameters
        #reset Sim
        if not ResetQ.empty():
            if ResetQ.get() == True:
                points, springs = Reset(springLength, num, k, startAngle, damping)
            else:
                running = False

        #Pause/Play sim
        if not PlayQ.empty():
            PlayQ.get()
            Play = not Play
            
        #Update spring length
        if not lenQ.empty():
            springLength = lenQ.get()
            points, springs = Reset(springLength, num, k, startAngle, damping)
        
        #Update spring constant
        if not kQ.empty():
            k = kQ.get()
            springs[0].SetSpringConstant(k) 

        #Update points num
        if not numQ.empty():
            num = numQ.get()
            points, springs = Reset(springLength, num, k, startAngle, damping)

        #Update start angle
        if not angleQ.empty():
            startAngle = angleQ.get()
            points, springs = Reset(springLength, num, k, startAngle, damping)

        #Update Damping Amount
        if not dampQ.empty():
            damping = dampQ.get()
            points[0].SetDamping(damping)
        
        #checking for quiting of application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        pygame.display.update() #update screen

    pygame.quit()


if __name__ =="__main__":
    Run(0,0,0,0,0,0,0)

    
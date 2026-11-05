import pygame
import Point
import Spring
from UI_Elements import Button
import pickle

pygame.init()
#Create screen
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("Soft Body Editor")
clock = pygame.time.Clock()

#Create buttons
addVerticies = Button(pygame.Vector2(60,50), "Point", (211, 138, 50), 25)
SaveObject = Button(pygame.Vector2(540,50), "Save", (50, 211, 77), 25)
LoadObject = Button(pygame.Vector2(540,110), "Load", (50, 211, 203), 25 )

def SaveShape(points, springs):
    #Write data to file
    for p in points:
        p.SetGravityConstant(0.5)
    f = open("CustomObject\\Name.pkl", "wb")
    #write to file
    pickle.dump(points,f)
    pickle.dump(springs,f)
    f.close()

def LoadShape(Filename):
    #Load data from file
    f = open("CustomObject\\"+ Filename + ".pkl", "rb")
    points = pickle.load(f)
    springs = pickle.load(f)
    f.close()    
    return points, springs   


verticies = []
springs = []
k = 150

placeVerticies = False
selected = True
selectedpoints = []

running = True

while running:
    screen.fill((92, 92, 92))
    clock.tick(60)

    #Check for buttons clicked
    if addVerticies.OnClick():
        placeVerticies = not placeVerticies
    elif LoadObject.OnClick():
        verticies, springs = LoadShape("Name")
    elif SaveObject.OnClick():
        SaveShape(verticies,springs)
    #If buttons are not pressed
    elif pygame.mouse.get_pressed()[0] and selected == True:
        #place point
        if placeVerticies == True:
            pointPos = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            point = Point.PointMass(pointPos,pygame.Vector2(0,0), 5, False)
            verticies.append(point)
        #Select point
        elif placeVerticies == False:
            mouseVector = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            if len(selectedpoints) < 2:
                for i in verticies:
                    dist = mouseVector - i.pos
                    length = dist.magnitude()
                    if length <= 5:
                        selectedpoints.append(i)
        selected = False
    elif not pygame.mouse.get_pressed()[0]:
        selected = True

    #Draw points and springs
    for p in verticies:
        p.Draw(screen)
    for s in springs:
        s.Draw(screen)

    #check for two selected points
    if len(selectedpoints) == 2:
        a = selectedpoints[0]
        b = selectedpoints[1]
        valid = True
        #check if the two selected points are valid
        for s in springs:
            if (a.pos == s.a.pos and b.pos == s.b.pos) or (b.pos == s.a.pos and a.pos == s.b.pos):
                valid = False
        #create and append spring
        if valid == True:
            dist = (a.pos-b.pos).magnitude()
            springs.append(Spring.Spring(dist, a,b))
        selectedpoints = []

    #draw selected points in different colour
    for i in selectedpoints:
        pygame.draw.circle(screen, (255,255,0), i.pos, 5)

    #Draw buttons
    addVerticies.Draw(screen)
    SaveObject.Draw(screen)
    LoadObject.Draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

    
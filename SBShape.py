import pygame


class SBShape():
    #constructor
    def __init__(self, points, springs):
        self.points = points
        self.springs = springs

    def Draw(self, screen):
        #loop through springs
        for s in self.springs:
            s.Draw(screen)
        #loop through points
        for p in self.points:        
            p.Draw(screen)

    def Update(self,screen):
        #updates the points
        for p in self.points:         
            p.Update(screen)
        #updates the springs
        for s in self.springs:
            s.Update()
    


class Cloth(SBShape):
    TearConstant = 2.75
    #Constructor
    def __init__(self, points, springs):
        super().__init__(points, springs)
    
    #overwriting the shape draw method
    def Draw(self, screen):
        #loop through springs
        for s in self.springs:
            if s.a == None or s.b == None:
                self.springs.remove(s)
            else:
                length = (s.a.pos - s.b.pos).magnitude()
                #clamp magnitude
                if length > 55:
                    length = 55
                if length < 10:
                    length = 10
                
                #Map range calculation to normalise values
                #Y = (X-A)/(B-A) * (D-C) + C
                stretch = (length-10)/(55-10) * (1-0) + 0 

                red = pygame.Color(255,0,0)
                green = pygame.Color(0,255,0)
                #lerp through the two colours based on the stretch of the spring
                s.colour = pygame.Color.lerp(green, red, stretch)
                s.Draw(screen)

        #loop through points
        for i in range(0, len(self.points)):
            for j in range(0, len(self.points[i])):          
                self.points[i][j].Draw(screen)


    #overwriting the main spring method
    def Update(self):
        tearLength = self.springs[0].restLength * Cloth.TearConstant
        #updates the points
        for i in range(0, len(self.points)):
            for j in range(0, len(self.points[i])):          
                self.points[i][j].Update()
        #updates the springs
        for s in self.springs:
            if s.a == None or s.b == None:
                self.springs.remove(s)
            elif (s.a.pos - s.b.pos).magnitude() > tearLength:
                self.springs.remove(s)            
            else:

                s.Update()

    def SetTearConstant(self, nTear):
        Cloth.TearConstant = nTear
    



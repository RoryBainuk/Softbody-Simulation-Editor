import pygame

class Spring():
    damping = 5
    k = 150
    stiffness = 6

    #constructor
    def __init__(self, restLength, a, b, colour = (0,255,0), IsExternal=True):
        self.restLength = restLength
        #a and b are PointMass objects
        self.a = a
        self.b = b
        self.colour = colour
        self.isExternal = IsExternal

    #physics calculations to apply forces to the two points respective to their distance
    #https://en.wikipedia.org/wiki/Hooke%27s_law
    def Update(self):
        #find distance between two points
        vec = self.a.pos - self.b.pos
        vecLength = vec.length()
        vecNormalised = vec.normalize()

        moveLength = self.restLength - vecLength

        #calculate force with damping
        springForce = moveLength * Spring.stiffness

        velDiff = self.b.vel - self.a.vel
        dot = vecNormalised.dot(velDiff)
        dampingForce = 0.5 * dot * Spring.damping

        totalForce = springForce + dampingForce
        totalForce = pygame.math.clamp(totalForce, -1000, 1000)


        #apply forces to points
        self.a.vel += vecNormalised * totalForce / Spring.k
        self.b.vel -= vecNormalised * totalForce / Spring.k

    #Draw spring
    def Draw(self, screen):
        pygame.draw.aaline(screen, self.colour, self.a.pos, self.b.pos) 

    def SetSpringConstant(self, newK):
        Spring.k = newK

    def SetStiffness(self, newStif):
        Spring.stiffness = newStif

    def SetDamping(self, newDamp):
        Spring.damping = newDamp



class ClothSpring(Spring):
    def __init__(self, restLength, a, b, colour=(0, 255, 0), IsExternal=True):
        super().__init__(restLength, a, b, colour, IsExternal)
    
    def Update(self):
        force = self.a.pos - self.b.pos
        x = force.magnitude() - self.restLength
        if force.magnitude() == 0:
            force = pygame.Vector2(0,0)
        else:
            force.normalize()

        force = force * (Spring.k * x)
        self.b.accel += force   
        force = force * -1
        self.a.accel += force


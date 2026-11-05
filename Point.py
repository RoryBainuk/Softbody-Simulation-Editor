import pygame

class PointMass():
    #Class variables
    gravityConstant = 0.5
    minBounce = 2
    dampingFactor = 1
    frictionFactor = 1

    #Constructor
    def __init__(self, pos, vel, radius, locked=False):
        #Initialise attributes
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.colour = (255,0,0)
        self.accel = pygame.Vector2(0, PointMass.gravityConstant)
        self.locked = locked

    def Update(self, screen):
        #collision with floor
        if self.pos.y < screen.get_height() - self.radius:
            self.vel.y += self.accel.y
        else:
            if self.vel.y > PointMass.minBounce:
                self.vel.y *= -1 * PointMass.dampingFactor
            elif abs(self.vel.y) <= PointMass.minBounce:
                self.vel.y = 0

        #collision with walls
        if (self.pos.x < self.radius and self.vel.x < 0) or (self.pos.x > screen.get_width() - self.radius and self.vel.x > 0):
            self.vel.x *= -1 * PointMass.dampingFactor

            if abs(self.vel.x) <= PointMass.minBounce:
                self.vel.x = 0
        # adding friction
        if self.vel.y == 0 and self.vel.x != 0:
            if self.vel.x > 0:
                self.vel.x -= PointMass.frictionFactor
            elif self.vel.x < 0:
                self.vel.x += PointMass.frictionFactor

        if self.locked:
            self.vel = pygame.Vector2(0,0)

        #updating position
        self.pos += self.vel

    #Draw Point to the screen
    def Draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.pos, self.radius)


    #Change colour of point
    def SetColour(self, newColour):
        self.colour = newColour

    def SetGravityConstant(self, newG):
        PointMass.gravityConstant = newG

class ClothPoint(PointMass):
    damping = 0.99
    def __init__(self, pos, vel, radius, locked=False):
        super().__init__(pos, vel, radius, locked)

    def Update(self):
        if not self.locked:
            self.accel += pygame.Vector2(0, PointMass.gravityConstant)
            self.vel *= ClothPoint.damping
            self.vel += self.accel
            self.pos += self.vel
            self.accel = self.accel * 0

    def SetDamping(self, ndamp):
        ClothPoint.damping = ndamp


import pygame
pygame.init()
pygame.font.init()

class Button():
    #Text margin in percentage
    margin = 30
    
    #Constructor
    def __init__(self, pos, text, colour, scale):
        self.pos = pos
        self.colour = colour
        self.click = False

        #creating font and text for button
        Font = pygame.font.SysFont('Arial', scale, True)
        self.text = Font.render(text, True, (0,0,0))

        #calculating button width and height with margins
        self.width = self.text.get_width() * (1 + (Button.margin/100))
        self.height = self.text.get_height() * (1 + (Button.margin/100))

    #Draw Method
    def Draw(self, screen):
        mousePos = pygame.Vector2(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

        #Draw Button Body
        buttonX = self.pos.x - (self.width / 2)
        buttonY = self.pos.y - (self.height / 2)
        buttonBody = pygame.Rect(buttonX, buttonY, self.width, self.height)

        #Check if mouse position is hovering over body
        HoverX = mousePos.x >= buttonBody.left and mousePos.x <= (buttonBody.left + buttonBody.width)
        HoverY = mousePos.y >= buttonBody.top and mousePos.y <= (buttonBody.top + buttonBody.height)
        if HoverX and HoverY:
            #Check if Mouse clicked and colour the mouse accordingly
            if pygame.mouse.get_pressed()[0]:
                colour = (self.colour[0] - 100, self.colour[1] - 100, self.colour[2] - 100)
                pygame.draw.rect(screen, colour, buttonBody)
            else:
                colour = (self.colour[0] - 50, self.colour[1] - 50, self.colour[2] - 50)
                pygame.draw.rect(screen, colour, buttonBody) 
        else:
            pygame.draw.rect(screen, self.colour, buttonBody) 


        #calculate text position to the center of the button body
        textPos = (buttonX + (buttonBody.width/2) - (self.text.get_width() / 2), 
                   buttonY + (buttonBody.height/2)- (self.text.get_height() / 2))

        #draw text
        screen.blit(self.text, textPos)

    #Method which returns true when the button is pressed
    def OnClick(self):
        mousePos = pygame.Vector2(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

        buttonX = self.pos.x - (self.width / 2)
        buttonY = self.pos.y - (self.height / 2)
        buttonBody = pygame.Rect(buttonX, buttonY, self.width, self.height)

        #Check if mouse position is hovering over body
        HoverX = mousePos.x >= buttonBody.left and mousePos.x <= (buttonBody.left + buttonBody.width)
        HoverY = mousePos.y >= buttonBody.top and mousePos.y <= (buttonBody.top + buttonBody.height)

        #Check Button press conditions
        if HoverX and HoverY and self.click == False and pygame.mouse.get_pressed()[0]:
            self.click = True
            #button click event
            return True
        if not pygame.mouse.get_pressed()[0]:
            self.click = False
        if pygame.mouse.get_pressed()[0] and (not(HoverX) or not(HoverY)):
            self.click = True

        return False
    

if __name__ == "__main__":
    screen = pygame.display.set_mode((600,600), pygame.RESIZABLE) #create a pygame screen that is resizable
    pygame.display.set_caption("Simulation Enviroment")
    clock = pygame.time.Clock() #create a clock for controlling fps
    running = True
    test = Button(pygame.Vector2(300,300), "Button", (150,255,150), 100)


    #MAIN LOOP
    while running:
        clock.tick(60)

        #fill screen with background colour
        screen.fill((50,50,50)) 

        test.Draw(screen)
        
        if test.OnClick():
            print("clicked")

        #checking for quiting of application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        pygame.display.update() #update screen

    pygame.quit()
        
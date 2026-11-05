import pygame
pygame.init()

def mapRange(num, inMin, inMax, outMin, outMax):
    return outMin + ((num - inMin) / (inMax - inMin) * (outMax - outMin))

class Button():
    #Text margin in percentage
    margin = 30
    
    #Constructor
    def __init__(self, pos, text, colour, scale, textColour = (0,0,0)):
        self.pos = pos
        self.colour = colour
        self.click = False

        #creating font and text for button
        Font = pygame.font.SysFont('Arial', scale, True)
        self.text = Font.render(text, True, textColour)

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
                colour = (pygame.math.clamp(self.colour[0] - 100, 0, 255), pygame.math.clamp(self.colour[1] - 100, 0, 255), pygame.math.clamp(self.colour[2] - 100, 0, 255))
                pygame.draw.rect(screen, colour, buttonBody, border_radius=5)
            else:
                colour = (pygame.math.clamp(self.colour[0] - 50, 0, 255), pygame.math.clamp(self.colour[1] - 50, 0, 255), pygame.math.clamp(self.colour[2] - 50, 0, 255))
                pygame.draw.rect(screen, colour, buttonBody, border_radius=5) 
        else:
            pygame.draw.rect(screen, self.colour, buttonBody, border_radius=5) 


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


class Slider():

    #Class attributes
    edgeColour = (0,50,50)
    fillColour = (0,150,150)
    KnobColour = (53, 83, 255)

    Font = pygame.font.SysFont('Arial', 20, True)

    #Constructor
    def __init__(self, lower, upper, default, width, height, pos, continuous=False):
        self.lower = lower
        self.upper = upper
        self.width = width
        self.height = height
        self.pos = pos
        self.value = default
        self.continuous = continuous

        self.edge = pygame.Rect(self.pos.x - self.width/2, self.pos.y - self.height/2, self.width, self.height)
        self.box = pygame.Rect(self.pos.x - self.width/2 - 40, self.pos.y - 15, 30, 30)

        #Text box attributes
        self.boxText = str(default)
        self.active = False
        self.text = Slider.Font.render(self.boxText, True, (0,0,0))


    #Update the slider
    def Update(self, events):
        #get mouse position
        mousePos = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        #Check if mouse is held down
        if pygame.mouse.get_pressed()[0]:
            #Check cursor is in the bounds of the slider body
            if self.edge.collidepoint(mousePos):
                #Calculate new value
                newValue = mapRange((mousePos.x - self.edge.left), 0, self.width, self.lower, self.upper)
                newValue = pygame.math.clamp(newValue, self.lower, self.upper)
                #Update slider value
                if not self.continuous:
                    self.value = round(newValue)
                else:
                    self.value = round(newValue, 1)

            #Set the condition for updating the text box
            else:
                if self.box.collidepoint(mousePos):
                    self.active = True
                else:
                    self.active = False
                    if not self.continuous:
                        self.value = int(self.boxText)
                    else:
                        self.value = float(self.boxText)

        for event in events:
            #Update value if enter is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.active = False
                if not self.continuous:
                    self.value = int(self.boxText)
                else:
                    self.value = float(self.boxText)

            #check for keyboard inputs
            if event.type == pygame.KEYDOWN and self.active == True:
                if event.key == pygame.K_BACKSPACE: #check for backspace
                    self.boxText = self.boxText[:-1]
                #check if the keyboard input is a number and that the number isnt too long
                elif (event.unicode).isdigit() and len(self.boxText) < len(str(self.upper)):
                    self.boxText += event.unicode

        #clamp slider value
        self.value = pygame.math.clamp(self.value, self.lower, self.upper)

        #update text to slider value
        if not self.active:
            self.boxText = str(self.value)
        self.text = Slider.Font.render(self.boxText, True, (0,0,0))

    def GetValue(self):
        return self.value


    def Draw(self, screen):

        #DRAW SLIDER 
        fillAmount = (self.value - self.lower) / (self.upper - self.lower) * (self.width)

        fillAmount = mapRange(self.value, self.lower, self.upper, 0, self.width)

        #Body fill
        body = pygame.Rect(self.pos.x - self.width/2, self.pos.y - self.height/2, fillAmount, self.height)
        pygame.draw.rect(screen, Slider.fillColour, body, border_radius= 3)

        #Body edge
        pygame.draw.rect(screen, Slider.edgeColour, self.edge, 3, 5)

        #Knob
        knobPos = pygame.Vector2(body.right, self.pos.y)
        pygame.draw.circle(screen, Slider.KnobColour, knobPos, self.height / 1.9)

        #DRAW TEXTBOX
        pygame.draw.rect(screen, (255,255,255), self.box)
        textPos = (self.box.left + (self.box.width/2) - (self.text.get_width() / 2), 
                   self.box.top + (self.box.height/2) - (self.text.get_height() / 2))

        #draw text
        screen.blit(self.text, textPos)




class Textbox():

    #Constructor
    def __init__(self, width, height, pos, fillerText = "", maxCharacters = -1, NumsOnly = False):
        self.width = width
        self.height = height
        self.pos = pos
        self.body = pygame.Rect(self.pos.x - self.width/2, self.pos.y - self.height/2, self.width, self.height)
        self.font = pygame.font.SysFont('Arial', int(self.height // 2), True)

        #set the max number of characters that can be entered
        self.maxCharacters = maxCharacters

        self.numsOnly = NumsOnly

        #display attributes
        self.fillerText = fillerText
        self.boxText = ""
        self.active = False
        self.text = self.font.render(self.boxText, True, (200,200,200))

    def Update(self, events):
        #get mouse position
        mousePos = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        #Check if mouse is held down
        if pygame.mouse.get_pressed()[0]:
            #Set the condition for updating the text box
            if self.body.collidepoint(mousePos):
                self.active = True
            else:
                self.active = False

        for event in events:
            #Update value if enter is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.active = False

            #check for keyboard inputs
            if event.type == pygame.KEYDOWN and self.active == True:
                #calculate the width of the current text with an added margin
                tempWidth = self.font.render(self.boxText + "WW", True, (0,0,0)).get_width()

                if event.key == pygame.K_BACKSPACE: #check for backspace
                    self.boxText = self.boxText[:-1]

                #limit the length of the text in the box
                if self.numsOnly:
                    if tempWidth < self.body.width and self.maxCharacters == -1 and (event.unicode).isdigit():
                        self.boxText += event.unicode
                    elif len(self.boxText) < self.maxCharacters and self.maxCharacters != -1 and (event.unicode).isdigit():
                        self.boxText += event.unicode
                else:
                    if tempWidth < self.body.width and self.maxCharacters == -1:
                        self.boxText += event.unicode
                    elif len(self.boxText) < self.maxCharacters and self.maxCharacters != -1:
                        self.boxText += event.unicode

        #Set the text to the filler text if there is no input
        if self.boxText == "":
            self.text = self.font.render(self.fillerText, True, (200,200,200))            
        else:
            self.text = self.font.render(self.boxText, True, (0,0,0))


    def Draw(self, screen):
        #Draw body
        pygame.draw.rect(screen, (255,255,255), self.body, border_radius=4)
        pygame.draw.rect(screen, (0,0,0), self.body, 2, 4)

        #Draw text
        textPos = (self.body.left + 15, self.body.top + (self.body.height/2) - (self.text.get_height() / 2))
        screen.blit(self.text, textPos)


    #Getters and setters for use in future development
    def GetText(self):
        return self.boxText

    def SetText(self, nText):
        self.boxText = nText
        

print("UI_Elements imported!")


if __name__ == "__main__":
    screen = pygame.display.set_mode((600,600), pygame.RESIZABLE) #create a pygame screen that is resizable
    pygame.display.set_caption("Simulation Enviroment")
    clock = pygame.time.Clock() #create a clock for controlling fps
    running = True
    textbox = Textbox(300, 50, pygame.Vector2(300,300), fillerText="Enter Text", NumsOnly=True)
    slider = Slider(50, 100, 75, 300, 30, pygame.Vector2(300, 100))
    button = Button(pygame.Vector2(300,500), "Button", (100,200,100), 50)

    #MAIN LOOP
    while running:
        clock.tick(60)

        events = pygame.event.get()

        #fill screen with background colour
        screen.fill((150,150,150)) 

        textbox.Draw(screen)
        textbox.Update(events)
        
        slider.Draw(screen)
        slider.Update(events)

        button.Draw(screen)

        if button.OnClick():
            print("clicked")

        #checking for quiting of application
        for event in events:
            if event.type == pygame.QUIT:
                running = False


        pygame.display.update() #update screen

    pygame.quit()

    
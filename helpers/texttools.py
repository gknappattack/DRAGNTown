import pygame

class TextRectException:
    def __init__(self, message=None):
            self.message = message

    def __str__(self):
        return self.message

def multiLineSurface(string: str, font: pygame.font.Font, rect: pygame.rect.Rect, fontColour: tuple, BGColour: tuple, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Parameters
    ----------
    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rect style giving the size of the surface requested.
    fontColour - a three-byte tuple of the rgb value of the
             text color. ex (0, 0, 0) = BLACK
    BGColour - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                1 horizontally centered
                2 right-justified

    Returns
    -------
    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """

    finalLines = []
    requestedLines = string.splitlines()
    # Create a series of lines that will fit on the provided
    # rectangle.
    for requestedLine in requestedLines:
        if font.size(requestedLine)[0] > rect.width:
            words = requestedLine.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException("The word " + word + " is too long to fit in the rect passed.")
            # Start a new line
            accumulatedLine = ""
            for word in words:
                testLine = accumulatedLine + word + " "
                # Build the line while the words fit.
                if font.size(testLine)[0] < rect.width:
                    accumulatedLine = testLine
                else:
                    finalLines.append(accumulatedLine)
                    accumulatedLine = word + " "
            finalLines.append(accumulatedLine)
        else:
            finalLines.append(requestedLine)

    # Let's try to write the text out on the surface.
    surface = pygame.Surface(rect.size)
    surface.fill(BGColour)
    accumulatedHeight = 0
    for line in finalLines:
        if accumulatedHeight + font.size(line)[1] >= rect.height:
             raise TextRectException("Once word-wrapped, the text string was too tall to fit in the rect.")
        if line != "":
            tempSurface = font.render(line, 1, fontColour)
        if justification == 0:
            surface.blit(tempSurface, (0, accumulatedHeight))
        elif justification == 1:
            surface.blit(tempSurface, ((rect.width - tempSurface.get_width()) / 2, accumulatedHeight))
        elif justification == 2:
            surface.blit(tempSurface, (rect.width - tempSurface.get_width(), accumulatedHeight))
        else:
            raise TextRectException("Invalid justification argument: " + str(justification))
        accumulatedHeight += font.size(line)[1]
    return surface


class TextBox:
    def __init__(self, screen, height, width, pos=(0,0)):
        self.screen = screen
        self.height = height  #100
        self.width = width #480
        self.pos_x = pos[0] #260
        self.pos_y = pos[1] #505
        self.text = []
        self.font = pygame.font.SysFont('Arial', 20)
        self.text_color = (0,0,0)
        self.page = 0
        self.page_end = 0
        #self.text_input = TextBox(self.screen, 30, self.width, (self.pos_x,self.pos_y + 5))

    def draw(self):
        color = (50,50,50)
        #if self.active:
        #    color = (150, 150, 150)
        #else:
        #    color = (50, 50, 50)
        pygame.draw.rect(self.screen, color, pygame.Rect(self.pos_x, self.pos_y, self.width, self.height))
        #self.screen.blit(self.font.render(self.text, True, self.text_color), (self.pos_x + 2, self.pos_y))
        self.screen.blit(multiLineSurface(self.formatText(), self.font, pygame.Rect(self.pos_x, self.pos_y, self.width, self.height), (0,0,0), (100,100,100)), (self.pos_x + 2, self.pos_y))
        
    def formatText(self):
        display_text = ""
        for i in range(self.page, self.page_end + self.page):
            display_text += self.text[i] + "\n"
        return display_text

    def updateText(self, input):
        print(self.text)
        self.text.append(input)
        self.page_end += 1
        if self.page_end % 6 == 0:
            self.page += 4
            self.page_end = 2
        #if len(self.text)*20 % self.width - 3  < 1:
        #self.text += '\n'
        
class TextInput(TextBox):
    def __init__(self, screen, height, width, pos=(0,0)):
        TextBox.__init__(self, screen, height, width, pos)
        self.active = False
        self.isCaps = False
        self.text = ""
    def draw(self, ):
        color = (0,0,0)
        if self.active:
            color = (0, 255, 0)
            if self.isCaps:
                color = (0, 125, 70)
        else:
            color = (255, 0, 0)
        pygame.draw.rect(self.screen, color, pygame.Rect(self.pos_x, self.pos_y, self.width, self.height))
        self.screen.blit(multiLineSurface(self.text, self.font, pygame.Rect(self.pos_x, self.pos_y, self.width, self.height), (0,0,0), color), (self.pos_x + 2, self.pos_y))
    
    def updateText(self, input):
        self.text += input

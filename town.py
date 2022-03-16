#from curses import KEY_ENTER
import pygame, time
import numpy as np
from pygame.locals import *
WIDTH = 760
HEIGHT = 640
#file = 'tmw_desert_spacing.png'
file = './Assets/Pixel Art Top Down - Basic/Texture/TX Tileset Grass.png'
#file = './Assets/top-down-collection-pack/Topview Fantasy Patreon Collection/Top-Down-Town/top-down-town-preview.png'
file2 = './Assets/Pixel Art Top Down - Basic/Texture/TX Struct.png'
file3 = './Assets/Pixel Art Top Down - Basic/Texture/TX Tileset Wall.png'
# Version = '2.0'

import pygame,sys
from pygame.locals import *

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

def sprite_sheet(size,file,pos=(0,0)):
    #Initial Values
    len_sprt_x,len_sprt_y = size #sprite size
    sprt_rect_x,sprt_rect_y = pos #where to find first sprite on sheet

    sheet = pygame.image.load(file).convert_alpha() #Load the sheet
    sheet_rect = sheet.get_rect()
    print('sr: ', sheet_rect)
    sprites = []
    print (sheet_rect.height, sheet_rect.width)
    for i in range(0,sheet_rect.height,size[1]):#rows # removed -len_sprt_y
        print ("row")
        for j in range(0,sheet_rect.width,size[0]):#columns # removed -len_sprt_x
            print ("column")
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
            sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
            sprites.append(sprite)
            sprt_rect_x += len_sprt_x

        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0
    print (sprites)
    return sprites

#VERSION HISTORY

    #1.1 - turned code into useable function

    #2.0 - fully functional sprite sheet loader

class Player(pygame.sprite.Sprite):
    def __init__(self, appearance, isPlayer, customPos, screen, cPx=0, cPy=0):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.isPlayer = isPlayer
        self.sheet = sprite_sheet((32,32), appearance)
        print(self.sheet)
        self.move_state = 0
        #self.image = pygame.image.load(sheet[0]).convert()
        self.image = self.sheet[1]
        # 0 walk down
        # 1 stand down
        # 2 stand left
        # 3 walk left
        # 4 walk right
        # 5 stand right

        self.rect = self.image.get_rect()
        if customPos:
            self.rect.center = (cPx, cPy)
        else:
            self.rect.center = (WIDTH / 2, HEIGHT / 2)
    
    def check_contact(self, input_character_rect_points):
        input_character_rect_points = np.array(input_character_rect_points)
        myPoints = np.array([self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright])
        result = np.abs(myPoints - input_character_rect_points)
        in_talking_dist = False
        #print("result: ", result)
        for i in result:
            if i[0] < 32 and i[1] < 32:
                in_talking_dist = True
        if in_talking_dist:
            return True
        else:
            return False
    
    def talk(self, message):
        #len(message)
        font_size = 10
        rect_width = 6 * font_size
        rect_height = 15
        pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(self.rect.topright[0], self.rect.topright[1], rect_width, rect_height))
        self.screen.blit(multiLineSurface(message[0:13] + "..", pygame.font.SysFont('Arial', font_size), pygame.Rect(self.rect.topright[0], self.rect.topright[1], rect_width, rect_height), (0,0,0), (255,255,255)), (self.rect.topright[0]+2, self.rect.topright[1]))

        # NOW I NEED TO SEND THIS TO THE SERVER
        # RETURN THE RESPONSE AND DISPLAY IT FOR THE CHARACTER
        return message

    def walk(self, sprite_vals):
        if self.move_state == 0:
                self.image = self.sheet[sprite_vals[2]]
                self.move_state = 1
        elif self.move_state == 1:
            self.image = self.sheet[sprite_vals[2]]
            self.move_state = 2
        elif self.move_state == 2:
            self.image = self.sheet[sprite_vals[1]]
            self.move_state = 3
        elif self.move_state == 3:
            self.image = self.sheet[sprite_vals[1]]
            self.move_state = 4
        elif self.move_state == 4:
            self.image = self.sheet[sprite_vals[0]]
            self.move_state = 5
        elif self.move_state == 5:
            self.image = self.sheet[sprite_vals[0]]
            self.move_state = 6
        elif self.move_state == 6:
            self.image = self.sheet[sprite_vals[1]]
            self.move_state = 7
        else:
            self.image = self.sheet[sprite_vals[1]]
            self.move_state = 0

    def update(self, input):
        if input == 'r':
            if (self.rect.x + 2) not in self.unvailablePixels:
                self.walk([6, 7, 8])
                self.rect.x += 2
                if self.rect.left > WIDTH:
                    self.rect.right = 0
        elif input == 'l':
            self.walk([3, 4, 5])
            self.rect.x -= 2
            if self.rect.right < 0:
                self.rect.left = WIDTH
        elif input == 'u':
            self.walk([9, 10, 11])
            self.rect.y -= 2
            if self.rect.bottom < 0:
                self.rect.top = HEIGHT
        elif input == 'd':
            self.walk([0, 1, 2])
            self.rect.y += 2
            if self.rect.top > HEIGHT:
                self.rect.bottom = 0
        elif input == 'st':
            1+1

    def setOOB(self, unavailablePixels):
        self.unvailablePixels = unavailablePixels
class Tileset:
    def __init__(self, file, size=(32, 32), margin=0, spacing=0):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()


    def load(self):

        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing
        
        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'

class Tilemap:
    def __init__(self, tileset, size=(30, 30), rect=None): # normally (10, 20)
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)

        h, w = self.size
        self.image = pygame.Surface((32*w, 32*h))
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def render(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j*32, i*32))

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        #firstrow = np.array([12,43,34,35,36,37,38,39,40,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39])
        #self.map[0] = firstrow
        print(self.map)
        print(self.map.shape)
        self.render()
    
    def set_matrix(self, input):
        self.map = input # 40 x 40
        self.render()
    
    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        print(self.map)
        self.render()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'      

class Game:
    #W = 960 # normally 640
    #H = 840 # normally 240
    SIZE = WIDTH, HEIGHT
    # SET A CLOCK
    
    def check_if_player_by_characters(self):
        the_player = self.all_sprites.sprites()[0]
        the_characters = self.all_sprites.sprites()[1:]
        player_points = np.array([the_player.rect.topleft, the_player.rect.topright, the_player.rect.bottomleft, the_player.rect.bottomright])
        talking_character_pos = None
        for i in range(len(the_characters)):
            isContact = the_characters[i].check_contact(player_points)
            if isContact:
                if self.input_box.active == False:
                    the_characters[i].talk("Press E")
                talking_character_pos = i + 1
        return talking_character_pos
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Game.SIZE)

        pygame.display.set_caption("Pygame Tiled Demo")
        self.all_sprites = pygame.sprite.Group()
        player = Player('./Assets/characters/PIPOYA FREE RPG Character Sprites 32x32/Male/Male 01-1.png', True, False, self.screen)
        villiager1 = Player('./Assets/characters/PIPOYA FREE RPG Character Sprites 32x32/Male/Male 02-2.png', False, True, self.screen, 200, 400)
        villiager2 = Player('./Assets/characters/PIPOYA FREE RPG Character Sprites 32x32/Female/Female 01-1.png', False, True, self.screen, 232, 400)
        villiager3 = Player('./Assets/characters/PIPOYA FREE RPG Character Sprites 32x32/Male/Male 03-1.png', False, True, self.screen, 264, 400)
        villiager4 = Player('./Assets/characters/PIPOYA FREE RPG Character Sprites 32x32/Male/Male 05-3.png', False, True, self.screen, 296, 400)

        self.all_sprites.add(player)
        self.all_sprites.add(villiager1)
        self.all_sprites.add(villiager2)
        self.all_sprites.add(villiager3)
        self.all_sprites.add(villiager4)

        # ------------ CHAT FUNCTIONALITY ----------------
        self.text_box = TextBox(self.screen, 120,760, (0,480))
        self.input_box = TextInput(self.screen, 30, 760, (0, 605))
        self.isCAPS = False
        self.displayChatCnt = 0
        self.chatBeingDisplayed = False
        self.displayChatTxt = ""
        self.talking_character_pos = None
        # ------------------------------------------------

        oobList = [(self.all_sprites.sprites()[1].rect.x, self.all_sprites.sprites()[1].rect.y)]
        print("oobList: ", oobList)
        player.setOOB(oobList)

        self.running = True
        self.clock = pygame.time.Clock()
        self.text_active = False
        self.user_text = ""
        self.base_font = pygame.font.Font(None, 30)

    def update_map(self):
        #self.load_image(file) # works
        tileset = Tileset(file)
        tilemap = Tilemap(tileset)
        #structures = sprite_sheet((32, 32), file2)
        tileset2 = Tileset(file2)
        tileset3 = Tileset(file3)
        #tilemap2 = Tilemap(tileset2)
        #tilemap.set_random() # works
        #---------------------------- For other map .png
        ROAD = 12
        WHT_CTR_FLWR = 33
        YLW_CTR_FLWR = 34
        WHT_CTR_SCTR = 35
        WHT_SCTR = 42
        YLW_SCTR = 43
        
        #RD_LFT_TRE_ML = 35
        #RD_LFT_TRE_BL = 36
        #RD_RL_TRE_TL = 37
        #RD_LFT = 38
        #RD_LFT = 39
        custommap = np.array([[ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD],\
        [ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD],\
        [ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD],\
        [ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD],\
        [ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,ROAD,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,ROAD,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,ROAD,ROAD,ROAD,ROAD,ROAD,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,ROAD,ROAD,ROAD,ROAD,ROAD,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD],\
        [0,0,0,0,0,0,0,0,0,0,ROAD,ROAD,ROAD,ROAD,ROAD,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,ROAD,ROAD,ROAD,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,ROAD,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        #[0,0,0,0,0,0,0,0,0,0,0,0,ROAD,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        #[0,0,0,0,0,0,0,0,0,0,0,0,ROAD,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [YLW_SCTR,0,0,0,0,0,0,0,0,YLW_SCTR,0,0,ROAD,0,0,YLW_SCTR,0,0,0,0,0,0,0,YLW_SCTR,0,0,0,0,0,0],\
        [0,0,0,YLW_SCTR,0,0,YLW_SCTR,0,0,0,0,YLW_SCTR,ROAD,0,0,0,0,0,0,0,YLW_SCTR,0,0,0,0,0,0,YLW_SCTR,0,0]])#,\
        
        #[0,0,0,0,0,0,0,0,0,0,0,0,ROAD,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])#,\
        #[0,0,0,0,0,0,0,0,0,0,0,0,ROAD,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        #[ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD],\
        #[YLW_SCTR,0,0,0,0,0,0,0,0,YLW_SCTR,0,0,ROAD,0,0,YLW_SCTR,0,0,0,0,0,0,0,YLW_SCTR,0,0,0,0,0,0],\
        #[0,0,0,YLW_SCTR,0,0,YLW_SCTR,0,0,0,0,YLW_SCTR,ROAD,0,0,0,0,0,0,0,YLW_SCTR,0,0,0,0,0,0,YLW_SCTR,0,0],\
        #])
        #------------------------------
        #print(tileset.rect.size)
        """custommap = np.array([[39,35,36,37,38,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,RD_LFT_TRE_ML,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,RD_LFT,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        ])"""
        #tilemap.set_zero()
        tilemap.set_matrix(custommap)
        #tilemap.set_random()
        
        # --------------- MAIN BACKGROUND ---------------
        self.screen.blit(tilemap.image, (0, 0))
        # --------------- LEFT STAIR --------------------
        LFT_STR_TOP = 17
        LFT_STR_MID = 18
        LFT_STR_BOT = 19
        LFT_STR_TOP_B = 21
        LFT_STR_MID_B = 22
        LFT_STR_BOT_B = 23
        RGT_STR_TOP = 33
        RGT_STR_MID = 34
        RGT_STR_BOT = 35

        self.screen.blit(tileset3.tiles[113], (32*0, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*0, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*1, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*1, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*2, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*2, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*3, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*3, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*4, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*4, 32*6))

        self.screen.blit(tileset2.tiles[LFT_STR_TOP], (32*5, 32*5))
        self.screen.blit(tileset2.tiles[LFT_STR_MID], (32*5, 32*6))
        self.screen.blit(tileset2.tiles[LFT_STR_MID], (32*5, 32*7))
        self.screen.blit(tileset2.tiles[LFT_STR_BOT], (32*5, 32*8))
        self.screen.blit(tileset2.tiles[RGT_STR_TOP], (32*6, 32*5))
        self.screen.blit(tileset2.tiles[RGT_STR_MID], (32*6, 32*6))
        self.screen.blit(tileset2.tiles[RGT_STR_MID], (32*6, 32*7))
        self.screen.blit(tileset2.tiles[RGT_STR_BOT], (32*6, 32*8))
        
        self.screen.blit(tileset3.tiles[113], (32*7, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*7, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*8, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*8, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*9, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*9, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*10, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*10, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*11, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*11, 32*6))
        #---------------
        self.screen.blit(tileset3.tiles[113], (32*12, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*12, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*13, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*13, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*14, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*14, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*15, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*15, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*16, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*16, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*17, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*17, 32*6))
        #---------------
        self.screen.blit(tileset3.tiles[113], (32*17, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*17, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*18, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*18, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*19, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*19, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*20, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*20, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*21, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*21, 32*6))

        self.screen.blit(tileset2.tiles[LFT_STR_TOP], (32*18, 32*5))
        self.screen.blit(tileset2.tiles[LFT_STR_MID], (32*18, 32*6))
        self.screen.blit(tileset2.tiles[LFT_STR_MID], (32*18, 32*7))
        self.screen.blit(tileset2.tiles[LFT_STR_BOT], (32*18, 32*8))
        self.screen.blit(tileset2.tiles[RGT_STR_TOP], (32*19, 32*5))
        self.screen.blit(tileset2.tiles[RGT_STR_MID], (32*19, 32*6))
        self.screen.blit(tileset2.tiles[RGT_STR_MID], (32*19, 32*7))
        self.screen.blit(tileset2.tiles[RGT_STR_BOT], (32*19, 32*8))
        
        self.screen.blit(tileset3.tiles[113], (32*20, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*20, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*21, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*21, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*22, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*22, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*23, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*23, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*24, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*24, 32*6))
        self.screen.blit(tileset3.tiles[113], (32*25, 32*5))
        self.screen.blit(tileset3.tiles[114], (32*25, 32*6))
        
        self.all_sprites.draw(self.screen)
        self.text_box.draw()
        self.input_box.draw()
        pygame.display.update()

    def update_ui(self, event):
        #self.input_rect = pygame.Rect(600, 650, 350, 170)
        self.text_box.draw()
        self.input_box.draw()
        #color_active = pygame.Color("lightskyblue")
        #color_active = pygame.Color("gray15")
        #color_passive = pygame.Color("black")
        #color_passive = pygame.Color("gray15")
        #color = color_passive
        if event != None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.text_active = True
            print(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # stores text except last letter
                    self.user_text = self.user_text[0:-1]
                elif event.key == pygame.K_RETURN:
                    self.text_active = not self.text_active
                else:
                    self.user_text += event.unicode
        
        #pygame.draw.rect(self.screen, color, self.input_rect)
        
        #text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))
        #self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        #self.input_rect.w = max(100, text_surface.get_width() + 10)
        pygame.display.flip()

    def run(self):
        right_pressed = False
        left_pressed = False
        up_pressed = False
        down_pressed = False
        while self.running:
            self.talking_character_pos = self.check_if_player_by_characters()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    self.update_ui(None)
                    if self.input_box.active == False:
                        if event.key == K_l:
                            self.update_map()
                        elif event.key == K_RIGHT:
                            right_pressed = True
                        elif event.key == K_LEFT:
                            left_pressed = True
                        elif event.key == K_UP:
                            up_pressed = True
                        elif event.key == K_DOWN:
                            down_pressed = True
                        #elif event.key == K_ESCAPE:
                            #self.input_box.active = False
                        #elif event.key == K_RETURN:
                            #self.input_box.active = True
                        elif event.key == K_e and self.talking_character_pos != None:
                            self.input_box.active = True
                            self.input_box.text = "Plr->{x}:".format(x=self.talking_character_pos)
                    else:
                        if event.key == K_LSHIFT:
                            self.isCAPS = not self.isCAPS
                            self.input_box.isCaps = not self.input_box.isCaps
                        if event.key == K_ESCAPE:
                            self.input_box.active = False
                            self.input_box.text = ""
                        if event.key == K_BACKSPACE and len(self.input_box.text) > 0:
                            self.input_box.text = self.input_box.text[:len(self.input_box.text)-1]
                        if event.key == K_RETURN:
                            self.chatBeingDisplayed = True
                            self.text_box.updateText(self.input_box.text)
                            self.displayChatTxt = self.input_box.text
                            self.input_box.text = ""
                            return_message = self.all_sprites.sprites()[0].talk(self.displayChatTxt)
                            self.all_sprites.sprites()[self.talking_character_pos].talk("{}->Plr: ".format(self.talking_character_pos) + return_message[7:])
                            self.text_box.updateText("{}->Plr: ".format(self.talking_character_pos) + return_message[7:])
                        if event.key == K_UP or event.key == K_DOWN or event.key == K_RIGHT or event.key == K_LEFT:
                            self.input_box.active = False
                            self.input_box.text = ""
                            continue
                        if event.key != K_BACKSPACE and event.key != K_ESCAPE and event.key != K_RETURN and event.key != K_LSHIFT:
                            if self.isCAPS:
                                print(event.key)
                                if (chr(event.key).isalpha()):
                                    self.input_box.updateText(chr(event.key - 32))
                                elif (chr(event.key) == '/'):
                                    self.input_box.updateText('?')
                                elif (chr(event.key) == ';'):
                                    self.input_box.updateText(':')
                                elif (chr(event.key) == '\''):
                                    self.input_box.updateText('\"')
                                elif (chr(event.key).isdigit()):
                                    if (chr(event.key == '1')):
                                        self.input_box.updateText('!')
                                    elif (chr(event.key == '2')):
                                        self.input_box.updateText('@')
                                    elif (chr(event.key == '3')):
                                        self.input_box.updateText('#')
                                    elif (chr(event.key == '4')):
                                        self.input_box.updateText('$')
                                    elif (chr(event.key == '5')):
                                        self.input_box.updateText('%')
                                    elif (chr(event.key == '6')):
                                        self.input_box.updateText('^')
                                    elif (chr(event.key == '7')):
                                        self.input_box.updateText('&')
                                    elif (chr(event.key == '8')):
                                        self.input_box.updateText('*')
                                    elif (chr(event.key == '9')):
                                        self.input_box.updateText('(')
                                    elif (chr(event.key == '0')):
                                        self.input_box.updateText(')')
                                    elif (chr(event.key == ',')):
                                        self.input_box.updateText('<')
                                    elif (chr(event.key == ',')):
                                        self.input_box.updateText('>')
                            else:
                                self.input_box.updateText(chr(event.key))
                
                elif event.type == KEYUP:
                    self.update_ui(None)
                    if event.key == K_RIGHT:
                        right_pressed = False
                    if event.key == K_LEFT:
                        left_pressed = False
                    if event.key == K_UP:
                        up_pressed = False
                    if event.key == K_DOWN:
                        down_pressed = False

                #if event.type == pygame.MOUSEBUTTONDOWN:
                #    self.update_ui(event)
                #    if self.input_rect.collidepoint(event.pos):
                #        self.text_active = True
                    

            if right_pressed:
                print(self.all_sprites.sprites())
                self.all_sprites.sprites()[0].update('r')
                self.update_map()
                self.update_ui(None)
                
            if left_pressed:
                print(self.all_sprites.sprites())
                self.all_sprites.sprites()[0].update('l')
                self.update_map()
                self.update_ui(None)
                
            if up_pressed:
                print(self.all_sprites.sprites())
                self.all_sprites.sprites()[0].update('u')
                self.update_map()
                self.update_ui(None)
                
            if down_pressed: 
                print(self.all_sprites.sprites())
                self.all_sprites.sprites()[0].update('d')
                self.update_map()
                self.update_ui(None) 
                
            
            if self.chatBeingDisplayed:
                self.displayChatCnt += 1
            
            if self.displayChatCnt == 40:
                self.displayChatCnt = 0
                self.chatBeingDisplayed = False

            self.clock.tick(20)  
            self.update_ui(None)     
        pygame.quit()

    def load_image(self, file):
        self.file = file
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()

        self.screen = pygame.display.set_mode(self.rect.size)
        pygame.display.set_caption(f'size:{self.rect.size}')
        self.screen.blit(self.image, self.rect)
        pygame.display.update()

game = Game()
game.run()
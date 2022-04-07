#from curses import KEY_ENTER
import pygame,sys,time
import numpy as np
from pygame.locals import *
from helpers.character_asset_holder import CharacterAssetHolder

from helpers.player import Player
from helpers.sprite_sheet import sprite_sheet
from helpers.texttools import TextBox, TextInput, multiLineSurface
from helpers.tiles import Tilemap, Tileset

WIDTH = 760
HEIGHT = 640
#file = 'tmw_desert_spacing.png'
file = './Assets/Pixel Art Top Down - Basic/Texture/TX Tileset Grass.png'
#file = './Assets/top-down-collection-pack/Topview Fantasy Patreon Collection/Top-Down-Town/top-down-town-preview.png'
file2 = './Assets/Pixel Art Top Down - Basic/Texture/TX Struct.png'
file3 = './Assets/Pixel Art Top Down - Basic/Texture/TX Tileset Wall.png'
# Version = '2.0'


class Game:
    #W = 960 # normally 640
    #H = 840 # normally 240
    SIZE = WIDTH, HEIGHT
    CHAR_ASST_IDX = 0
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

        pygame.display.set_caption("DRAGN Town")
        self.all_sprites = pygame.sprite.Group()
        player = Player(CharacterAssetHolder().getSprite(self.CHAR_ASST_IDX), True, False, self.screen)
        villiager1 = Player(CharacterAssetHolder().getSprite(50), False, True, self.screen, cPx=200, cPy=400)
        villiager2 = Player(CharacterAssetHolder().getSprite(23), False, True, self.screen, 232, 400)
        villiager3 = Player(CharacterAssetHolder().getSprite(35), False, True, self.screen, 264, 400)
        villiager4 = Player(CharacterAssetHolder().getSprite(46), False, True, self.screen, 296, 400, chatbot_address='/chatbot/trevor')
        villiager5 = Player(CharacterAssetHolder().getSprite(99), False, True, self.screen, 328, 400, chatbot_address='/chatbot/kevin')

        self.all_sprites.add(player)
        self.all_sprites.add(villiager1)
        self.all_sprites.add(villiager2)
        self.all_sprites.add(villiager3)
        self.all_sprites.add(villiager4)
        self.all_sprites.add(villiager5)


        # ------------ CHAT FUNCTIONALITY ----------------
        self.text_box = TextBox(self.screen, 125,760, (0,480))
        self.input_box = TextInput(self.screen, 34, 760, (0, 605))
        self.isCAPS = False
        self.displayChatCnt = 0
        self.chatBeingDisplayed = False
        self.displayChatTxt = ""
        self.talking_character_pos = None
        # ------------------------------------------------

        # -------------------- TESTING OUT OF BOUNDS (NON FUNCTIONAL) ----------------------
        oobList = [(self.all_sprites.sprites()[1].rect.x, self.all_sprites.sprites()[1].rect.y)]
        print("oobList: ", oobList)
        player.setOOB(oobList)
        # ----------------------------------------------------------------------------------

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

        ROAD = 12
        WHT_CTR_FLWR = 33
        YLW_CTR_FLWR = 34
        WHT_CTR_SCTR = 35
        WHT_SCTR = 42
        YLW_SCTR = 43

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

    # THIS FUNCTION COULD BE DISSOLVED INTO SOMETHING ELSE? USED ONLY FOR TEXT?
    def update_ui(self, event):
        self.text_box.draw()
        self.input_box.draw()

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
                        
                        # FOR DISPLAYING HELP
                        elif event.key == K_h:
                            self.text_box.updateText("HELP: Change character skin: ,<left> .<right> *move after  |  Scroll Console Text: [<up> ]<down>")

                        # FOR CHANGING CHARACTER
                        elif event.key == K_COMMA:
                            self.CHAR_ASST_IDX -= 1
                            self.all_sprites.sprites()[0].change_sprite(CharacterAssetHolder().getSprite(self.CHAR_ASST_IDX))
                            self.update_map()
                            self.update_ui(None)
                            self.clock.tick(20) 
                        elif event.key == K_PERIOD:
                            self.CHAR_ASST_IDX += 1
                            self.all_sprites.sprites()[0].change_sprite(CharacterAssetHolder().getSprite(self.CHAR_ASST_IDX))
                            self.update_map()
                            self.update_ui(None)
                            self.clock.tick(20) 
                        # FOR ALTERING DISPLAY PAGE
                        elif event.key == K_LEFTBRACKET:
                            self.text_box.decrease_page()
                        elif event.key == K_RIGHTBRACKET:
                            self.text_box.increase_page()

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
                            self.all_sprites.sprites()[0].chatbot_address = self.all_sprites.sprites()[self.talking_character_pos].chatbot_address
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
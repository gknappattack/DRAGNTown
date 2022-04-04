import pygame
import numpy as np
from helpers.server_communicator import ServerCommunicator
from helpers.sprite_sheet import sprite_sheet
from helpers.texttools import multiLineSurface
WIDTH = 760
HEIGHT = 640
DRAGN_SERVER_IP = "127.0.0.1"
DRAGN_SERVER_PORT = "8088"

class Player(pygame.sprite.Sprite):
    def __init__(self, appearance, isPlayer, customPos, screen, cPx=0, cPy=0, chatbot_address="/chatbot/echo"):
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
        self.chatbot_address = chatbot_address

        self.rect = self.image.get_rect()
        if customPos:
            self.rect.center = (cPx, cPy)
        else:
            self.rect.center = (WIDTH / 2, HEIGHT / 2)
    
    def change_sprite(self, appearance):
        self.sheet = sprite_sheet((32,32), appearance)
    
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
        self.screen.blit(multiLineSurface(message[0:7] + "..", pygame.font.SysFont('Arial', font_size), pygame.Rect(self.rect.topright[0], self.rect.topright[1], rect_width, rect_height), (0,0,0), (255,255,255)), (self.rect.topright[0]+2, self.rect.topright[1]))

        if self.isPlayer:
            sc = ServerCommunicator(DRAGN_SERVER_IP, DRAGN_SERVER_PORT, self.chatbot_address)
            message = sc.send_recv_server(message)["text"]
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

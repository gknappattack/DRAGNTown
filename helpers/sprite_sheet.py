import pygame

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

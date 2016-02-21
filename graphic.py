import pygame
from functions import singleton

@singleton
class ImageStorage(object):
    def __init__(self):
        self.cache = {}
        self.load('images/Actor1.png',32,32,'actor1')
        self.load('images/Actor2.png',32,32,'actor2')
        self.load('images/Actor3.png',32,32,'actor3')
        self.load('images/Evil.png',32,32,'evil')
        self.load('images/exit.png',19,20,'icon-exit')
        self.load('images/craft.png',20,20,'icon-craft')
        self.load('images/backpack.png',20,20,'icon-backpack')
        self.load('images/1.png',30,30,'flower')
        self.load('images/tilee4.png',30,30,'plants')
        self.load('images/tilee4_2.png',30,30,'plants_2')
        
    def __getitem__(self, key):
        return self.cache[key]
            
    def load(self,filename,width,height,key):
        self.cache[key] = self.__load_tile_table(filename,width,height)

    def __load_tile_table(self, filename, width, height):
        """Load an image and split it into tiles."""

        image = pygame.image.load(filename).convert_alpha()
        image_width, image_height = image.get_size()

        tile_table = []
        for tile_x in range(0, image_width/width):
            line = []
            tile_table.append(line)
            for tile_y in range(0, image_height/height):
                rect = (tile_x*width, tile_y*height, width, height)
                line.append(image.subsurface(rect))
        return tile_table
        
@singleton
class Camera(object):
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.screen_width = 600
        self.screen_height = 600
        self.world_width = 12900
        self.world_height = 12900
        #get world size from map class
        self.update((1220,1230))
            
    def update(self,(x,y)):
        #x,y - logic coords of player (he is in screen center)

        start_x = max(x - self.screen_width / 2,0)
        start_y = max(y - self.screen_height / 2,0)
        start_x = min(x - self.screen_width / 2,
                      self.world_width-self.screen_width)
        start_y = min(y - self.screen_height / 2,
                      self.world_height-self.screen_height)
        
        self.dx = start_x 
        self.dy = start_y
      

                          
    def coord_transform(self,(x,y)):
        #logic to screen
        return (x-self.dx,y-self.dy)
        
    def coord_transform_x(self,x):
        return x-self.dx
        
    def coord_transform_y(self,y):
        return y-self.dy
        
class Character_Sprite(pygame.sprite.Sprite):
    GO_TOP = 3
    GO_LEFT = 1
    GO_RIGHT= 2
    GO_BOTTOM=0
    

    def __init__(self,image_sourse,x=0,y=0):
        pygame.sprite.Sprite.__init__(self)
        
        self.data = None
        self.pred_data_x = 0
        self.pred_data_y = 0 
         
        self.frames = ImageStorage()[image_sourse][0:3]
        #slice need if images contain more than 1 character
        self.frames.append(self.frames[1]) 
        #double center animation
        self.image = self.frames[0][0]
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.frame = 0
        self.orientation = self.GO_BOTTOM
        
        
    def update(self,animate=False):
        if hasattr(self,'data'):
            
            x,y = self.data.get_pos()

            dx = x - self.pred_data_x
            dy = y - self.pred_data_y
            

            a = 1 #dopusk k 0
            
            if dx > a:
                self.orientation = self.GO_RIGHT

            if dx < -a:
                self.orientation = self.GO_LEFT
  
            if -a <= dx <= a:
                if dy >= 0:
                    self.orientation = self.GO_BOTTOM
                if dy < 0:
                    self.orientation = self.GO_TOP
                    
            self.pred_data_x = x
            self.pred_data_y = y
            
            x,y = Camera().coord_transform((x,y))
                
        if animate:
            self.image = self.frames[self.frame][self.orientation]
            self.frame += 1
            self.frame = self.frame % 4
            self.rect.x = round(x)
            self.rect.y = round(y)



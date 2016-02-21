import pygame 
import graphic
from map import Map
from model import Game
from graphic import Camera
from graphic import ImageStorage


class UiController(object):

    def __init__(self):
        self.map_drawer = MapDrawer()
        
        self.game_field = UiGameField(self)
        self.game_panel = UiGamePanel(self)
        self.mini_map = UiMiniMap(self)
        self.inventory_panel = UiInventory(self)
        self.map_panel = UiMap(self)
        self.main_menu = UiMainMenu(self)
        self.exit_menu = UiExitMenu(self)
        self.exit_without_save = UiExitWithoutSave(self)
        self.pause_menu = UiPauseMenu(self)
        self.options_menu = UiOptionsMenu(self)
        self.load_menu = UiLoadMenu(self)
        self.save_menu = UiSaveMenu(self)
        
        self.visible_panels = []
        
    def do_action(self,event):
        for panel in self.visible_panels:
            action_accepted = panel.offer_action(event)
            if action_accepted:
                break
                
    def hide_all_panels(self):
        copy = self.visible_panels[:]
        for panel in copy:
            panel.set_unvisible()
            
    def go_to_main_menu(self):
        self.hide_all_panels()
        self.main_menu.set_visible()

    def go_to_play(self):
        self.hide_all_panels()
        Game().paused = False
        self.game_field.set_visible()
        self.mini_map.set_visible()
        self.game_panel.set_visible()
        
    def pause(self):
        self.pause_menu.set_visible()
        Game().paused = True
        
    def quick_save(self):
        pass
        
    def open_save_menu(self):
        pass
        
    def open_load_menu(self):
        pass
        
    def open_options_menu(self):
        pass
        
    def load_game(self):
        pass

    def ask_about_exit(self):
        self.exit_menu.set_visible()
        
    def ask_about_exit_without_save(self):
        self.exit_without_save.set_visible()
        
    def exit(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        
    def generate_new_map(self):
        self.map_drawer.map_generate()
        self.mini_map.prepare_image()
        self.map_panel.prepare_image()
        self.game_field.prepare_image()
        self.move_mini_map_to_player()
        
    def open_inventory(self):
        self.inventory_panel.set_visible()
        
    def open_map(self):
        self.map_panel.set_visible()
        
    def map_move(self,(x,y)):
        map_width = self.map_drawer.get_map_width()
        map_height = self.map_drawer.get_map_height()
        c = self.mini_map.width/self.mini_map.zoom
        self.mini_map.start_x = max(x - c / 2,0)
        self.mini_map.start_y = max(y - c / 2,0)
        self.mini_map.start_x = min(x - c / 2,map_width - c)
        self.mini_map.start_y = min(y - c / 2,map_height - c)
        self.mini_map.update_image()
        
    def player_keyboard_move(self,direction):
        player = Game().player
        if direction == 'up':
            player.order_to_go(0,-1)
        if direction == 'down':
            player.order_to_go(0,1)
        if direction == 'left':
            player.order_to_go(-1,0)
        if direction == 'right':
            player.order_to_go(1,0)
        Camera().update(player.get_pos())
        self.move_mini_map_to_player()
            
    def player_mouse_move(self,x,y):
        player = Game().player
        px,py = Camera().coord_transform(player.get_pos())
        dx = x - px
        dy = y - py
        norm = max(abs(dx),abs(dy))
        dx /= norm
        dy /= norm
        player.order_to_go(dx,dy)
        Camera().update(player.get_pos())
        self.move_mini_map_to_player()
        
    def move_mini_map_to_player(self):
        player_x,player_y = Game().player.get_pos()
        tile_size = self.game_field.tile_size
        self.map_move((player_x/tile_size,player_y/tile_size))

class Event(object):
    def __init__(self):
        self.clear()

    def __repr__(self):
        return '\n'.join(["%s: %s" % (k,v)
                         for k,v in self.__dict__.items()])
                         
    def clear(self):
        self.event_type = 'empty'
        self.direction = ''
        self.key = None
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
                         
    def get_pygame_event(self,event):
        self.clear()
            
        if event.type == pygame.KEYUP:
            self.event_type = 'key press'
            self.key = event.key
            
        if event.type == pygame.USEREVENT:
            self.event_type = event.code
            if event.code == 'keyboard direct':
                self.direction = event.direct
            if event.code == 'mouse direct':
                self.x,self.y = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            self.x,self.y = event.pos
            if event.button==1:
                self.event_type = 'left click'

            if event.button==3:
                self.event_type = 'right click'

        if event.type == pygame.MOUSEMOTION:
            self.x,self.y = event.pos
            #self.dx,self.dy = event.rel

            if event.buttons[0] == 1:
                self.event_type = 'drag'
                
            if event.buttons == (0,0,0):
                self.event_type = 'mouse move'

class UiPanel(object):
    def __init__(self,controller,
                      color=(255,0,0),
                      depth=0,visible=False, 
                      top=0,left=0,
                      width=100,height=100,):
        self.controller = controller
        self.visible = visible
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.depth = depth
        self.color = color
        self.data = None
        self.image = None
        
    def __repr__(self):
        return '%s' % self.__class__
        
    def offer_action(self,action):
        return False
        
    def draw(self):
        if self.image is None:
            self.prepare_image()
        else:
            self.update_image()
        return self.image
        
    def prepare_image(self):
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        
        font20 = pygame.font.Font(None, 20)
        
        if hasattr(self,'data'):
            for button in self.data:
 
                button.image1 = pygame.Surface((button.width, 
                                                button.height))
                button.image1.fill(button.color)
                    
                button.image2 = pygame.Surface((button.width,
                                                button.height))
                if not button.static:
                    r,g,b = button.color
                    color=(int(r*0.7),int(g*0.8),int(b*0.9))
                
                button.image2.fill(color)
                    
                if button.mode in ('image','text and image'):
                    image = ImageStorage()[button.image_sourse][0][0]
                    button.image1.blit(image,(0,0))
                    button.image2.blit(image,(0,0))
                    x,_ = image.get_size()
                else:
                     x = 0
                if button.mode in ('text','text and image'):
                    textImg = font20.render(button.caption, 1, (0,0,0))
                    button.image1.blit(textImg,(x+5,0));
                    button.image2.blit(textImg,(x+5,0));
                
                self.image.blit(button.image1,(button.left,button.top))
            
    def update_image(self):
        if hasattr(self,'data'):
            for button in self.data:
                self.image.blit(button.get_image(),(button.left,button.top))
        
        
    def set_visible(self):
        if self.visible:
            pass
        else:
            self.visible = True
            self.controller.visible_panels.append(self)
            self.controller.visible_panels.sort(key=lambda x: -x.depth)
            
    def set_unvisible(self):
        if self.visible:
            self.visible = False
            self.controller.visible_panels.remove(self)

class UiButton(object):
    def __init__(self,name,
                      mode,#text,image,text and image
                      top=0,left=0,
                      width=100,height=100,
                      image_sourse = '',
                      static = False,
                      color=(200,60,0)
                       ):
        self.name = name
        self.caption = name
        self.mode = mode
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.static = static
        self.color = color
        self.image_sourse = image_sourse
        self.image1 = None
        self.image2 = None
        self.state='main'
        
    def get_image(self):
        if self.state == 'main':
            return self.image1
        elif self.state == 'mouseover':
            return self.image2
            
    def is_mouse_over(self,x,y):
        ret = False
        if x in range(self.left,self.left+self.width):
            if y in range(self.top,self.top+self.height):
                ret = True
        return ret
    
class uiTable(object):
    pass
    
class UiGameField(UiPanel):
    def __init__(self,controller):
        self.tile_size=40
        self.controller = controller
        self.visible = False
        self.top = 0
        self.left = 0
        self.width = 600
        self.height = 600
        self.depth = 0
        self.color = (100,50,50)
        self.image = None
        self.data1 = {}
        self.data = []

    def prepare_image(self):
        self.image = pygame.Surface((self.width, self.height))
        
        self.a = pygame.sprite.Group(graphic.Character_Sprite('actor2'),
                                graphic.Character_Sprite('actor1'),
                                graphic.Character_Sprite('actor3'),
                                #graphic.Character_Sprite('evil'),
                                )
        i=0
        for sprite in self.a:
            sprite.data = Game().npcs[i]
            i +=1
        playersprite = graphic.Character_Sprite('evil')
        playersprite.data = Game().player
        self.a.add(playersprite)
        
        Camera().update(Game().player.get_pos())
        
        map_drawer = self.controller.map_drawer
        self.bg = map_drawer.get_all_map_image(self.tile_size)
        self.image.blit(self.bg,(-Camera().dx,-Camera().dy))

        self.data1 = map_drawer.prepare_map_objects(self.tile_size)
        
        '''test=ImageStorage()['plants']
        for i in range(len(test)):
            testrow=test[i]
            for j in range(len(testrow)):
                testimg = testrow[j]
                self.bg.blit(testimg,(i*40,j*40))'''

        self.a.draw(self.image)

            
    def update_image(self):
        if not Game().paused:
            if Game().counter % Game().animate_divider == 0:
                animate = True
            else:
                animate = False
                
            self.image.fill((0,0,0))#for clearing sprites
            self.a.clear(self.image,self.image)
            self.a.update(animate)
            
                                                    
            self.image.blit(self.bg,(-Camera().dx,-Camera().dy)) #pos bg
            
            
            #objects
            self.data=[]
            player_x,player_y = Game().player.get_pos()
            for y in range((player_y-self.height/2)/self.tile_size,
                           (player_y+self.height/2)/self.tile_size):
                for x in range((player_x-self.width/2)/self.tile_size,
                               (player_x+self.width/2)/self.tile_size):
                    if (x,y) in self.data1:
                        btn = self.data1[x,y]
                        self.data.append(btn)
                        img=btn.get_image()
                        self.image.blit(img,(x*self.tile_size-Camera().dx,y*self.tile_size-Camera().dy))
            
    

            
            self.a.draw(self.image)
            
    def offer_action(self,event):
        ret = False
        if event.event_type == 'keyboard direct':
            self.controller.player_keyboard_move(event.direction)
            ret = True
        if event.event_type == 'mouse direct':
            self.controller.player_mouse_move(event.x,event.y)
            ret = True

        if event.event_type == 'mouse move':
            for button in self.data:
                button.state = 'main'
                if button.is_mouse_over(event.x+Camera().dx,
                                        event.y+Camera().dy):
                    button.state = 'mouseover'
                    ret = True
        return ret

class UiGamePanel(UiPanel):
    def __init__(self,controller):
        self.controller = controller
        self.visible = False
        self.top = 565
        self.left = 5
        self.width = 400
        self.height = 30
        self.depth = 1
        self.color = (200,0,100)
        self.image = None
        self.data = [UiButton('inventory','image',5,5,100,25,'icon-backpack'),
                     UiButton('craft','text and image',5,115,100,25,'icon-craft'),
                     UiButton('exit','text',5,220,100,25),
                     ]
        
    def offer_action(self,event):
        ret = False
        if event.event_type == 'key press':
            if event.key in (27,19):
                self.controller.pause()
                ret = True
            if event.key in (105,):
                self.controller.open_inventory()
                ret = True
            if event.key in (109,):
                self.controller.open_map()
                ret = True
                
        if event.event_type == 'mouse move':
            for button in self.data:
                button.state = 'main'
                if button.is_mouse_over(event.x-self.left,
                                        event.y-self.top):
                    button.state = 'mouseover'
                    ret = True       
        return ret
        
class UiMap(UiPanel):
    def __init__(self,controller):
        self.controller = controller
        self.visible = False
        self.top = 85
        self.left = 42
        self.width = 513
        self.height = 513
        self.depth = 9
        self.color = (60,150,40)
        self.image = None
        self.zoom = 4
        self.data = None
        self.start_x=0
        self.start_y=0
        
    def prepare_image(self):
        self.image = pygame.Surface((self.width, self.height))
        map_drawer = self.controller.map_drawer
        self.all_map_image = map_drawer.get_all_map_image(self.zoom)
        self.image.blit(self.all_map_image,(0,0))

    def update_image(self):
        tile_size = self.controller.game_field.tile_size
        self.image.fill((0,0,0))
        player_x,player_y = Game().player.get_pos()

        pixel = pygame.Surface((self.zoom, self.zoom))
        pixel.fill((255,0,0))
        self.image.blit(self.all_map_image,(-self.start_x*self.zoom,
                                            -self.start_y*self.zoom))
        self.image.blit(pixel, 
                        ((player_x/tile_size-self.start_x)*self.zoom,
                         (player_y/tile_size-self.start_y)*self.zoom))
        
    def offer_action(self,event):
        ret = False
        if event.event_type == 'key press':
            if event.key in (27,109):
                self.set_unvisible()
                ret = True
                
        if event.event_type == 'left click':
            x = event.x-self.left
            y = event.y-self.top
            if x in range (0,self.width) and y in range (0,self.height):
                self.controller.map_move((x/self.zoom,y/self.zoom))
                ret = True
                
        if event.event_type == 'mouse direct':
            ret = True
                
        return ret
        
class UiMiniMap(UiMap):
    def __init__(self,controller):
        self.controller = controller
        self.visible = False
        self.top = 5
        self.left = 451
        self.width = 129
        self.height = 129
        self.depth = 1
        self.color = (200,0,100)
        self.data = None
        self.image = None
        self.zoom = 8
        self.start_x = 0
        self.start_y = 0
        
    def offer_action(self,event):
        ret = False
        if event.event_type == 'key press':
            if event.key in (32,):
                self.controller.generate_new_map()
                ret = True
                
        return ret

class MapDrawer(object):
    def __init__(self):
        self.__data=Map()

    def map_generate(self):
        self.__data.generate()
        
    def get_map_width(self):
        return self.__data.width
        
    def get_map_height(self):
        return self.__data.height
    
    def get_tile(self,size,value):
        
        waterline = self.__data.waterline
        
        if value <= waterline:
            color = (25, 25, value+75)
        elif value > waterline and value <= waterline + 10:
            color = (value+80, value+80, 100)
        elif value > waterline + 10 and value <= waterline + 40:
            color = (0, 255-value, 0)
        elif value > waterline + 40 and value <= 190:
            color = (0, 255-value, 0)
        elif value > 190:
            color = (255-value, 255-value, 255-value)
        tile = pygame.Surface((size, size))
        tile.fill(color)
        return tile
        
    def get_all_map_image(self,tile_size):
        
        waterline = self.__data.waterline
        map_width = self.__data.width
        map_height= self.__data.height
        map_data = self.__data.map
        
        all_map_image = pygame.Surface((tile_size * map_width, 
                                        tile_size * map_height))
        
        for y in range(0, map_height):
            for x in range(0, map_width):
                value = int(map_data[y][x])
                tile = self.get_tile(tile_size,value)
                all_map_image.blit(tile,(x*tile_size,y*tile_size))
                
        return all_map_image
        
    def get_all_map_from_storage(self,tile_size):
        
        waterline = self.__data.waterline
        map_width = self.__data.width
        map_height = self.__data.height
        map_data = self.__data.storage[self.data.name]
        
        all_map_image = pygame.Surface((tile_size * map_width, 
                                        tile_size * map_height))
        
        for y in range(0, map_height):
            for x in range(0, map_width):
                if not isinstance(map_data[y][x],list):
                    value = int(map_data[y][x])
                    tile = self.get_tile(tile_size,value)
                    all_map_image.blit(tile,(x*tile_size,y*tile_size))
                else:
                    square = map_data[y][x]
                    for i in range(0,len(square)):
                        for j in range(0,len(square)): 
                            value = int(square[i][j])
                            tile = self.get_tile(tile_size/len(square),value)
                            all_map_image.blit(tile,(x*tile_size+j*tile_size/len(square),y*tile_size+i*tile_size/len(square)))
        return all_map_image
        
    def prepare_map_objects(self,tile_size):
        objsd = {}
        #objsl = []
        for key,value in self.__data.objects_on_map.items():
            x,y = key
            button = UiButton(name=value,
                              mode='image',
                              top=y*tile_size,left=x*tile_size,
                              width=30,height=30,
                              image_sourse ='flower',
                              static=False,
                              color=(200,60,0))
            img_x=value/100
            img_y=value%100
            button.image1 = ImageStorage()['plants'][img_x][img_y]
            button.image2 = ImageStorage()['plants_2'][img_x][img_y]
            objsd[(x,y)]=button
            #objsl.append(button)
        #return (objsd,objsl)
        return objsd


class UiInventory(UiPanel):
    def __init__(self,controller):
        self.controller = controller
        self.visible = False
        self.top = 300
        self.left = 300
        self.width = 280
        self.height = 100
        self.depth = 2
        self.color = (200,100,0)
        #self.data = None
        self.image = None
        
    def offer_action(self,event):
        ret = False
        if event.event_type == 'key press':
            if event.key in (27,105):
                self.set_unvisible()
                ret = True
                
        return ret
    
class UiMainMenu(UiPanel):
    def __init__(self,controller):
        self.controller = controller
        self.visible = False
        self.top = 0
        self.left = 0
        self.width = 600
        self.height = 600
        self.depth = 0
        self.color = (100,100,0)
        self.image = None
        self.data = [UiButton('continue','text',100,250,100,25),
                     UiButton('new','text',140,250,100,25),
                     UiButton('load','text',180,250,100,25),
                     UiButton('options','text',220,250,100,25),
                     UiButton('exit','text',260,250,100,25),
                     ]
                
    def offer_action(self,event):
        ret = False
        if event.event_type == 'key press':
            if event.key in (32,13,112):
                self.controller.go_to_play()
                ret = True
            if event.key == 27:
                self.controller.ask_about_exit()
                ret = True
                
        if event.event_type == 'mouse move':
            for button in self.data:
                button.state = 'main'
                if button.is_mouse_over(event.x-self.left,
                                        event.y-self.top):
                    button.state = 'mouseover'
                    ret = True
                    
        if event.event_type == 'left click':
            for button in self.data:
                if button.is_mouse_over(event.x-self.left,
                                        event.y-self.top):
                    if button.name == 'continue':
                        self.controller.go_to_play()    
                        ret = True
                    if button.name == 'new':
                        self.controller.go_to_play()    
                        ret = True
                    if button.name == 'load':
                        self.controller.open_load_menu()    
                        ret = True
                    if button.name == 'options':
                        self.controller.open_options_menu()    
                        ret = True
                    if button.name == 'exit':
                        self.controller.ask_about_exit()    
                        ret = True
        return ret
    
class UiLoadMenu(UiPanel):
    def __init__(self,controller):
        self.controller = controller
        self.visible = False
        self.top = 100
        self.left = 150
        self.width = 300
        self.height = 400
        self.depth = 15
        self.color = (100,0,40)
        self.image = None
        
    def offer_action(self,event):
        ret = False
        if event.event_type == 'key press':
            if event.key in (27):
                self.set_unvisible()
                ret = True
                
        return ret
        
class UiSaveMenu(UiPanel):
    def __init__(self,controller):
        self.controller = controller
        self.visible = False
        self.top = 100
        self.left = 150
        self.width = 300
        self.height = 400
        self.depth = 15
        self.color = (60,50,40)
        self.image = None
        
    def offer_action(self,event):
        ret = False
        if event.event_type == 'key press':
            if event.key in (27):
                self.set_unvisible()
                ret = True
                
        return ret
    
class UiOptionsMenu(UiPanel):
    def __init__(self,controller):
        self.controller = controller
        self.visible = False
        self.top = 100
        self.left = 150
        self.width = 300
        self.height = 400
        self.depth = 15
        self.color = (50,0,140)
        self.image = None
        
    def offer_action(self,event):
        ret = False
        if event.event_type == 'key press':
            if event.key in (27):
                self.set_unvisible()
                ret = True
                
        return ret
            
class UiPauseMenu(UiPanel):
    def __init__(self,controller):
        self.controller = controller
        self.visible = False
        self.top = 100
        self.left = 150
        self.width = 300
        self.height = 400
        self.depth = 10
        self.color = (10,70,40)
        self.image = None
        self.data = [UiButton('continue','text',100,100,100,25),
                     UiButton('save','text',140,100,100,25),
                     UiButton('load','text',180,100,100,25),
                     UiButton('options','text',220,100,100,25),
                     UiButton('main menu','text',260,100,100,25),
                     ]
        
    def offer_action(self,event):
        ret = False
        if event.event_type == 'key press':
            if event.key in (27,19):
                self.controller.go_to_play()
                ret = True
        
        if event.event_type == 'mouse direct':
            ret = True        
            
        if event.event_type == 'mouse move':
            for button in self.data:
                button.state = 'main'
                if button.is_mouse_over(event.x-self.left,
                                        event.y-self.top):
                    button.state = 'mouseover'
                    ret = True
                    
        if event.event_type == 'left click':
            for button in self.data:
                if button.is_mouse_over(event.x-self.left,
                                        event.y-self.top):
                    if button.name == 'continue':
                        self.controller.go_to_play()
                        ret = True
                    if button.name == 'save':
                        self.controller.open_save_menu()    
                        ret = True
                    if button.name == 'load':
                        self.controller.open_load_menu()    
                        ret = True
                    if button.name == 'options':
                        self.controller.open_options_menu()    
                        ret = True
                    if button.name == 'main menu':
                        self.controller.ask_about_exit_without_save()   
                        ret = True
                
        return ret
            
class UiExitMenu(UiPanel):
    def __init__(self,controller):
        self.controller = controller
        self.visible = False
        self.top = 200
        self.left = 250
        self.width = 100
        self.height = 50
        self.depth = 20
        self.color = (0,0,40)
        self.image = None
        self.data = [UiButton('yes','text',20,20,25,25),
                     UiButton('no','text',20,65,25,25),
                     ]
        
    def offer_action(self,event):
        ret = False
        if event.event_type == 'key press':
            if event.key in (121,):
                self.controller.exit()
                ret = True
            if event.key in (27,110):
                self.set_unvisible()
                ret = True
                
        if event.event_type == 'mouse move':
            for button in self.data:
                button.state = 'main'
                if button.is_mouse_over(event.x-self.left,
                                        event.y-self.top):
                    button.state = 'mouseover'
                    ret = True
                    
        if event.event_type == 'left click':
            for button in self.data:
                if button.is_mouse_over(event.x-self.left,
                                        event.y-self.top):
                    if button.name == 'yes':
                        self.controller.exit()
                        ret = True
                    if button.name == 'no':
                        self.set_unvisible()
                        ret = True
        return ret
        
class UiExitWithoutSave(UiPanel):
    def __init__(self,controller):
        self.controller = controller
        self.visible = False
        self.top = 200
        self.left = 250
        self.width = 100
        self.height = 50
        self.depth = 20
        self.color = (0,20,20)
        self.image = None
        self.data = [UiButton('yes','text',20,20,25,25),
                     UiButton('no','text',20,65,25,25),
                     ]
    
    def offer_action(self,event):
        ret = False
        if event.event_type == 'key press':
            if event.key in (27):
                self.set_unvisible()
                ret = True
        
        if event.event_type == 'mouse move':
            for button in self.data:
                button.state = 'main'
                if button.is_mouse_over(event.x-self.left,
                                        event.y-self.top):
                    button.state = 'mouseover'
                    ret = True
                    
        if event.event_type == 'left click':
            for button in self.data:
                if button.is_mouse_over(event.x-self.left,
                                        event.y-self.top):
                    if button.name == 'yes':
                        self.controller.go_to_main_menu()
                        ret = True
                    if button.name == 'no':
                        self.set_unvisible()
                        ret = True
        return ret

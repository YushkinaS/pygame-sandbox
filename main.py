import pygame
from model import Game
import time
import ui

pygame.init()
resolution = (600, 600)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(resolution)

uic = ui.UiController()
ui_event = ui.Event()

uic.go_to_main_menu()
running = True

while running:

    clock.tick(Game().fps)
    if not Game().paused:
        Game().counter = (Game().counter + 1) % Game().fps
    
#############events#######################
    keys = pygame.key.get_pressed()
    if keys[119] or keys[273]:
        pygame.event.post(pygame.event.Event(pygame.USEREVENT,
                                             direct='up',
                                             code='keyboard direct'))
    if keys[115] or keys[274]:
        pygame.event.post(pygame.event.Event(pygame.USEREVENT,
                                             direct='down',
                                             code='keyboard direct'))
    if keys[100] or keys[275]:
        pygame.event.post(pygame.event.Event(pygame.USEREVENT,
                                             direct='right',
                                             code='keyboard direct'))
    if keys[97] or keys[276]:
        pygame.event.post(pygame.event.Event(pygame.USEREVENT,
                                             direct='left',
                                             code='keyboard direct'))
                                             
    if pygame.mouse.get_pressed()==(1,0,0):#drag without mousemotion
        pygame.event.post(pygame.event.Event(pygame.USEREVENT,
                                             pos=pygame.mouse.get_pos(),
                                             code='mouse direct'))
        
    for event in pygame.event.get():
        ui_event.get_pygame_event(event)
        uic.do_action(ui_event)
        if event.type == pygame.QUIT:
            running = False
#############logic########################
    if not Game().paused:
        Game().step()
#############draw#######################
    for panel in reversed(uic.visible_panels):
        screen.blit(panel.draw(), (panel.left,panel.top))
        
    pygame.display.flip()


'''
test_stats = {'hp': 100,
              'mp': 30,
              'armor': 0,
              'damage': 40, 
              'delay': 2,
              'x': 15,
              'y': 20,
              'level':1
              }

c = model.FightUnit('player',**test_stats)
d = model.FightUnit('monster1',**test_stats)
e = model.FightUnit('monster2',**test_stats)

fight = d.begin_fight(c)
e.set_active_target(c)
fight.add_fighter(e)

while fight.is_active():
   print fight
   fight.step()
   print '\n'
'''

pygame.quit()

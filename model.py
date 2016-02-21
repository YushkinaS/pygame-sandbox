import random
from functions import div_by_zero
from functions import singleton

@singleton
class Game(object):

    def __init__(self):
        self.counter = 0
        self.paused = True
        self.fps_animate = 10
        self.fps = 30
        self.animate_divider = self.fps/self.fps_animate
        self.player = FightUnit('4',x=120,y=130,speed = 20)
        self.npcs=[FightUnit('1',x=20,y=30,speed=4.4),
                   FightUnit('2',x=20,y=30,speed=3.4),
                   FightUnit('3',x=20,y=30,speed=2.4),
                   ]
        self.enviroment=[]
 
    
    def step(self):
        for npc in self.npcs:
            npc.step()


class FightUnit(object):
    
    neighbour = [(-1,0),
                 (-1,1),
                 (0,1),
                 (1,1),
                 (1,0),
                 (1,-1),
                 (0,-1),
                 (-1,-1)]
    
    def __init__(self, name, **args):
        self.name = name
        self.speed = 1
        self.x = 0.0
        self.y = 0.0
        self.program = self.program_go_to(1500,1500)
        self.active_target = None
        self.last_enemy = None
        for k,v in args.items():
            setattr(self,k,v)
            
    def __repr__(self):
        return '\n'.join(["%s: %s" % (k,v)
                         for k,v in self.__dict__.items()])
                         
    def step(self):
        self.program.next()
        
    def program_stay(self,ticks):
        while True:
            for i in range (1,ticks):
                yield None
            self.program = self.program_walking()

    def program_walking(self):
        while True:
            dx,dy = random.choice(self.neighbour)
            s = random.randrange(100)
            for i in range (1,s):
                self.x += dx*self.speed
                self.y += dy*self.speed
                yield None
                
            if not 0<self.x<600:
                self.program = self.program_go_to(1300,1300)
            if not 0<self.y<600:
                self.program = self.program_go_to(1300,1300)
        
    def program_go_to(self,x,y):
        while True:
            dy = div_by_zero(y - self.y,abs(y - self.y))
            dx = div_by_zero(x - self.x,abs(x - self.x))
            
            if abs(y - self.y)<2 and abs(x - self.x)<1:
                self.program = self.program_stay(300)
            
            self.x += dx*self.speed
            self.y += dy*self.speed
                    
            yield None

    def order_to_go(self,dx,dy):
        self.x+=dx*self.speed
        self.y+=dy*self.speed


    def get_stats(self):
        pass
        
    def get_pos(self):
        return (self.x,self.y)
    
    def attack(self):
        print self.name, ': arrgh!!!'
        if self.active_target is not None:
            self.active_target.be_attacked(self,Damage())
        else:
            print 'i have no target'
            self.fight.remove_fighter(self) 
   
    def be_attacked(self,enemy,damage):
        self.hp -= damage.power * (100 - self.armor)/100
        self.last_enemy = enemy
        print self.name,': i got %i %s damage' % (damage.power,
              damage.type),'my hp = ',self.hp
        if self.hp <=0:
            self.fight.remove_fighter(self)
            print self.name, 'is dead'

    def select_active_target(self):
        if self.last_enemy in self.fight.fighters:
            self.active_target = self.last_enemy
        else:
            self.active_target = None
 
    def set_active_target(self, target):
        self.active_target = target

    def begin_fight(self, target):
        self.set_active_target(target)
        target.set_active_target(self)
        return Fight([self,target])
        
class Damage(object):
    def __init__(self):
        self.type = 'physical'
        self.power = 30
    
class Fight(object):
    def __init__(self, fighters):   
        
        self.fighters = fighters
        self._iterator = 0
        for fighter in fighters:
            fighter.fight = self

    def __repr__(self):
        return 'In fight:' + ' '.join(
                  [fighter.name for fighter in self.fighters])
        
    def step(self):
        self.fighters[self._iterator].attack()
        self._iterator += 1
        self._iterator = self._iterator % len(self.fighters)

    def add_fighter(self,fighter):
        self.fighters.append(fighter)
        fighter.fight = self

    def remove_fighter(self,fighter):
        """Remove fighter from fighters list"""
        i = self.fighters.index(fighter)
        if i <= self._iterator:
            self._iterator -= 1
        del self.fighters[i]

        fighter.fight = None
        fighter.last_enemy = None
        
        for fighter in self.fighters:
            fighter.select_active_target()
        
    def is_active(self):
        if len(self.fighters) > 1:
            return True
        else:
            return False


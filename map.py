import random
from functions import limited_inc
from functions import random_mod
from functions import div_by_zero

class MapStorage(object):
    def __init__(self):
        self.cache = {}
        self.square_size = 4
        
    def __getitem__(self, key):
        if isinstance(self.cache[key],list):
            return self.cache[key]
        else:
            table = deepen(self.cache[key])
            self.cache[key] = table
            return self.cache[key]
        
    def storage_map(self,map_name,map_data):
        self.cache[map_name]=map_data[:]
        
    def deepen(self,value,objects=[]):
        table=[]
        for i in range(0,self.square_size):
            row=[]
            for j in range(0,self.square_size):
                row.append(value)
            table.append(row)
        return table
            
    def get_data(self,x,y,map_name='qwerty1'):
        #x,y - logic coords
        x_index = int(x / self.square_size)
        y_index = int(y / self.square_size)
        print x,y,x_index,y_index
        x = int(x % self.square_size)
        y = int(y % self.square_size)
        table=self[map_name]
        square=table[y_index][x_index]
        
        if not isinstance(square,list):
            square = self.deepen(square)
            table[y_index][x_index] = square
       
        data = square[y][x]
        return data
        

class Map:

    neighbour = [(-1,0),
                 (-1,1),
                 (0,1),
                 (1,1),
                 (1,0),
                 (1,-1),
                 (0,-1),
                 (-1,-1)]
                 
    #(code,quantity)
    objects = [(101,3),(102,1),
               (201,1),
               (301,5),(302,7),(303,9),
               (401,3),(402,6),(403,4),(404,4)]
    
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
             cls.instance = super(Game, cls).__new__(cls)
        return cls.instance
                     
    def __init__(self):
        self.storage=MapStorage()
        self.counter=0
        self.generate()
        
    def generate(self):
        self.width = 33
        self.height = 33
        self.waterline = 0
        self.map = []
        self.objects_on_map = {}
        self.counter+=1
        self.name = 'qwerty'+str(self.counter)
        self.__create_empty_map()

        #self.__generate_caves_and_routes(10)
        self.__diamond_square()
        
        self.walkable_coords = self.__pack()
        self.__place_for_something = self.walkable_coords[:]
        
        
        self.storage.storage_map(self.name,self.map)
        self.__plant_resourses_and_enemies(self.objects)
        
    def __create_empty_map(self):
        for y in range(0, self.height):
            map_row = []
            for x in range(0, self.width):
                r = 0
                map_row.append(r)
            self.map.append(map_row)
            
    def __smoothen(self):

        """A simple blurring function for the map. Gets rid of unwanted
           sharpness such as a single sand tile in the middle of a bunch
           of grass, etc."""

        for y in range(0, self.height):
            for x in range(0, self.width):
                average = 0.0
                times = 0.0

                if x - 1 >= 0:
                    average += self.map[y][x-1]
                    times += 1
                if x + 1 < self.width-1:
                    average += self.map[y][x+1]
                    times += 1
                if y - 1 >= 0:
                    average += self.map[y-1][x]
                    times += 1
                if y + 1 < self.height-1:
                    average += self.map[y+1][x]
                    times += 1

                if x - 1 >= 0 and y - 1 >= 0:
                    average += self.map[y-1][x-1]
                    times += 1
                if x + 1 < self.width and y - 1 >= 0:
                    average += self.map[y-1][x+1]
                    times += 1
                if x - 1 >= 0 and y + 1 < self.height:
                    average += self.map[y+1][x-1]
                    times += 1
                if x + 1 < self.width and y + 1 < self.height:
                    average += self.map[y+1][x+1]
                    times += 1

                average += self.map[y][x]
                times += 1

                average /= times

                self.map[y][x] = average

    def __get_waterline(self):

        values = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                values.append(self.map[y][x])
        values.sort()

        return values[int((len(values)-1)*.50)]

    def __pack(self):
        res = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.map[y][x] > self.waterline:
                    res.append((y,x))
        return res
        
    def __plant_something(self,something=5):
        place = random.choice(self.__place_for_something)
        y,x = place
        self.objects_on_map[(x,y)] = something
        #don't use setpoint! keep this data in another variable
        #if self._set_point(y,x,something):
         #   self._place_for_something.remove(place)
        
    def __random_points(self,count_of_points=1):
        """random coords in map"""
        points = []
        for i in range(count_of_points):
            y = random.randrange(self.height-1)
            x = random.randrange(self.width-1)
            points.append((y,x))
        return points
        
    def __set_point(self,y,x,value):
        try:
            self.map[y][x] = value
            return True
        except:

            self.__set_point_2(y,x,value)
            return False
            
    def __set_point_2(self,y,x,value):

        if y >= self.height-1:
            y = y % (self.height - 1)

        if x >= self.width-1:
            x = x % (self.width - 1)

        self.map[y][x] = value

    def __get_point(self,y,x):
        """y = y % (self.height - 1)
        x = x % (self.width - 1)
        return self.map[y][x] """
        
        try:
            value = self.map[y][x] 
            return value
        except:
            return random.random()
            
    def __diamond_square(self):
        self.map[0][0] = random.random()
        self.map[0][self.width-1] = random.random()
        self.map[self.height-1][0] = random.random()
        self.map[self.height-1][self.width-1] = random.random()
        
        squares = [(0,0)] #y1,x1
        a = self.width-1
        while a > 1:
            a = a/2
            diamonds = self.__square(squares,a)
            squares = self.__diamond(diamonds,a)

        self.__smoothen()
        
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.map[y][x] = self.map[y][x] * self.map[y][x] * 255
                
        self.waterline = self.__get_waterline()

    def __square(self,squares,a):
        diamonds = []
        for square in squares:
            y1,x1 = square
            
            mid = (self.__get_point(y1,x1)
                   + self.__get_point(y1,x1+2*a)
                   + self.__get_point(y1+2*a,x1)
                   + self.__get_point(y1+2*a,x1+2*a)
                   ) / 4
            self.__set_point(y1+a,x1+a,random_mod(mid,a/10+10))
            diamonds.append((y1+a,x1+a))
            
        return diamonds
        
    def __diamond(self,diamonds,a):
        squares = []
        for diamond in diamonds:
            y,x = diamond
            
            left = (self.__get_point(y,x)
                   + self.__get_point(y-a,x-a)
                   + self.__get_point(y,x-2*a)
                   + self.__get_point(y+a,x-a)
                   ) / 4
            self.__set_point(y,x-a,random_mod(left,a/10+10))
            squares.append((y,x-a))
            
            right = (self.__get_point(y,x)
                   + self.__get_point(y-a,x+a)
                   + self.__get_point(y,x+2*a)
                   + self.__get_point(y+a,x+a)
                   ) / 4
            self.__set_point(y,x+a,random_mod(right,a/10+10))
            squares.append((y,x))
            
            top = (self.__get_point(y,x)
                   + self.__get_point(y-a,x-a)
                   + self.__get_point(y-2*a,x)
                   + self.__get_point(y-a,x+a)
                   ) / 4
            self.__set_point(y-a,x,random_mod(top,a/10+10))
            squares.append((y-a,x))
            
            bottom = (self.__get_point(y,x)
                   + self.__get_point(y+a,x-a)
                   + self.__get_point(y+2*a,x)
                   + self.__get_point(y+a,x+a)
                   ) / 4
            self.__set_point(y+a,x,random_mod(bottom,a/10+10))
            squares.append((y-a,x-a))
            
        return squares
    
    def __generate_caves_and_routes(self,count_of_points=1):
        cave_centers = self.__random_points(count_of_points)
            
        predx = -1
        predy = -1
        for point in cave_centers:
            y,x = point
            if predx > 0:
                self.__dig_route((predy,predx),point)
            self.__dig_cave(y,x)
            self.__set_point(y,x,200)
            predy,predx = point

    def __dig_cave(self,start_y,start_x,size=100):
        s = size
        x = start_x
        y = start_y
        
        for point in self.neighbour:
            dy,dx = point
            self.__set_point(y+dy,x+dx,200)

    def __dig_route(self,start,finish):
        y1,x1 = start
        y2,x2 = finish
      
        dy = y2 - y1
        dx = x2 - x1
        
        abs_dy = abs(dy)
        abs_dx = abs(dx)
        
        napr_dy = div_by_zero(dy,abs_dy)
        napr_dx = div_by_zero(dx,abs_dx)
        
        x = 0
        y = 0
        while (y < abs_dy) or (x < abs_dx):
            napr = random.choice(('left','right'))   

            if napr == 'left':
                x = limited_inc(x,abs_dx)
            if napr == 'right':
                y = limited_inc(y,abs_dy)
                    
            self.__set_point(y1+y*napr_dy,x1+x*napr_dx,100)
    
    def __plant_resourses_and_enemies(self,plant_list=[]):
        for code,quantity in plant_list:
            for i in range(0,quantity):
                self.__plant_something(code)

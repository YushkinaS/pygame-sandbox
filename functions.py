import random

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance
    
def div_by_zero(x,y):
    if y == 0:
        return 0
    else:
        return x/y
        
def limited_inc(base,limit,inc=1):
    res = base + inc
    if res > limit:
        return limit
    else:
        return res

def random_mod(x,a):
    return x*(1+float(random.randrange(-a,a))/100)

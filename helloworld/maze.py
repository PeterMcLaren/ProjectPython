import random

#use tuple because immutable so faster
direction=((1,0),(-1,0),(0,-1),(0,1))

class block:
    #Class Attribute
    def __init__(self, colour, solid):
        self.colour=colour
        self.solid=solid

def displaygrid(grid):
    for i in range(0,len(grid)):
        for j in range(0,len(grid[i])):
            if grid[i][j].solid:
               print("@@",end="")
            else:
               print("  ",end="")
        print("")

def creategrid(x,y,colour,solid):
    grid=[]
    for _ in range(x):
        x=[]
        for _ in range(y):
            x.append(block(colour,solid))
        grid.append(x)
    return grid

def gofromhere(x,y,grid):
    tried=[False]*4
    grid[x][y].solid=False
    while False in tried:
        d=random.randrange(4)
        tried[d]=True
        dx=direction[d][0]
        dy=direction[d][1]
        if checkifsolid(x+dx*2,y+dy*2,grid):
            grid[x+dx][y+dy].solid=False
            gofromhere(x+dx*2,y+dy*2,grid)

def checkifsolid(x,y,grid):
    if x>0 and x<len(grid):
        if y>0 and y<len(grid[x]):
            return grid[x][y].solid
    return False

maze=creategrid(43,83,"black",True)
gofromhere(1,1,maze)
displaygrid(maze)

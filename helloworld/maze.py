class Block:
    #Class Attribute
    def __init__(self, colour, solid):
        self.colour=colour
        self.solid=solid

def displaygrid(grid):
    for i in range(0,len(grid)):
        for j in range(0,len(grid[i])):
            if grid[i][j].solid:
                print("X",end="")
        print("")

def creategrid(x,y,colour,solid):
    grid=[]
    for i in range(x):
        x=[]
        for j in range(y):
            x.append(Block(colour,solid))
        grid.append(x)
    return grid

mazesize=20
maze=creategrid(mazesize,mazesize,"black",True)
displaygrid(maze)

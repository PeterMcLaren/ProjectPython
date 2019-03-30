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

maze=[]
gridsize=20
 
for i in range(gridsize):
    x=[]
    for j in range(gridsize):
        x.append(Block("black",True))
    maze.append(x)

displaygrid(maze)

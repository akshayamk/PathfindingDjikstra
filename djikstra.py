import pygame, sys
import math


HEIGHT = 600
WIDTH = 1000
ROWS = 30
SQUARE_WIDTH = HEIGHT // ROWS
COLOUR_BLUE = (0, 153, 153)
COLOUR_YELLOW = (255, 255, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_BLACK = (0,0,0)
COLOUR_RED = (255,0,0)
COLOUR_GREEN = (0, 255, 0)
COLOUR_ORANGE = (255, 165 ,0)
COLOUR_TURQUOISE = (64, 224, 208)
COLOUR_PURPLE = (128, 0, 128)

class GUI:

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        self.initialise()
        
    
    def initialise(self):
        self.start = False
        self.end = False
        self.obstructions = []
        self.obstructions.clear()
        self.colour = COLOUR_WHITE
        self.startdraw()

    
    def startdraw(self):
        self.fill()
        self.drawgrid()
        self.drawUI()
    
    def fill(self):
        self.screen.fill(COLOUR_BLACK)
        
    def drawgrid(self):
        x = 0  
        y = 0  
        for sq in range(ROWS): 
            x = x + SQUARE_WIDTH
            y = y + SQUARE_WIDTH

            pygame.draw.line(self.screen, COLOUR_WHITE, (x,0),(x,HEIGHT))
            pygame.draw.line(self.screen, COLOUR_WHITE, (0,y),(HEIGHT,y))
    
    def drawUI(self):
        button = pygame.font.Font('freesansbold.ttf', 20)
        pygame.draw.rect(self.screen, COLOUR_WHITE, (700, 100, 50, 30))
        pygame.draw.rect(self.screen, COLOUR_WHITE, (850, 100, 100, 30)) 
        text = self.font.render("Start", 1 , COLOUR_BLACK)
        self.screen.blit(text, (705, 105))

        pygame.draw.rect(self.screen, COLOUR_WHITE, (700, 150, 50, 30))
        pygame.draw.rect(self.screen, COLOUR_WHITE, (850, 150, 100, 30)) 
        text = self.font.render("End", 1 , COLOUR_BLACK)
        self.screen.blit(text, (705, 155))

        #Map button
        pygame.draw.rect(self.screen, COLOUR_WHITE, (700, 200, 150, 30))
        maptext = button.render("Map", 1 , COLOUR_BLACK)
        self.screen.blit(maptext, (760, 205))

        #Clear button
        pygame.draw.rect(self.screen, COLOUR_WHITE, (700, 250, 150, 30))
        cleartext = button.render("Clear", 1 , COLOUR_BLACK)
        self.screen.blit(cleartext, (750, 255))

        #status
        pygame.draw.rect(self.screen, COLOUR_WHITE, (700, 300, 200, 60))

    
    def userinput(self, xpos, ypos):
        x = int(xpos // (SQUARE_WIDTH))
        y = int(ypos // (SQUARE_WIDTH))

        if not self.start:
            pygame.draw.rect(self.screen, COLOUR_YELLOW, (x * SQUARE_WIDTH, y * SQUARE_WIDTH, SQUARE_WIDTH + 1, SQUARE_WIDTH +1))
            self.startnode = (y, x)
            self.printstart(y, x)
        elif not self.end:
            pygame.draw.rect(self.screen, COLOUR_RED, (x * SQUARE_WIDTH, y * SQUARE_WIDTH, SQUARE_WIDTH + 1, SQUARE_WIDTH +1))
            self.endnode = (y,x)
            self.printend(y, x)
        else:
            #store obstructions coordinates
            pygame.draw.rect(self.screen, COLOUR_WHITE, (x * SQUARE_WIDTH, y * SQUARE_WIDTH, SQUARE_WIDTH + 1, SQUARE_WIDTH +1))
            self.obstructions.append((y,x))
    
    def printstart(self, x, y):

        pygame.draw.rect(self.screen, COLOUR_WHITE, (850, 100, 100, 30)) 
        makestr = '(' + (str(x)) + ',' + str(y) + ')'
        text = self.font.render(makestr, 1 , COLOUR_BLACK)
        self.screen.blit(text, (855, 105))

        self.start = True #start position set
    
    def printend(self, x, y):
        pygame.draw.rect(self.screen, COLOUR_WHITE, (850, 150, 100, 30)) 
        makestr = '(' + (str(x)) + ',' + str(y) + ')'
        text = self.font.render(makestr, 1 , COLOUR_BLACK)
        self.screen.blit(text, (855, 155))

        self.end = True
    
    def clearUI(self):
        self.initialise()
    
    def getstartnode(self):
        return self.startnode
    
    def getendnode(self):
        return self.endnode
    
    def getobstructions(self):
        return self.obstructions

class Draw:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('freesansbold.ttf', 18)
    
    def printstatus(self, solved):
        pygame.draw.rect(self.screen, COLOUR_WHITE, (700, 300, 200, 60))

        if solved:
            cleartext = self.font.render("Path solved!", 1 , COLOUR_BLACK)
            self.screen.blit(cleartext, (705, 305))
        else:
            cleartext = self.font.render("No path available!", 1 , COLOUR_BLACK)
            self.screen.blit(cleartext, (705, 305))

    
    def printpath(self, path):
        if len(path) > 0:
            for node in range(1, len(path)-1):
                y, x = path[node]
                pygame.draw.rect(self.screen, COLOUR_TURQUOISE, (x * SQUARE_WIDTH, y * SQUARE_WIDTH, SQUARE_WIDTH + 1, SQUARE_WIDTH +1))
                self.printstatus(True)
        else:
            self.printstatus(False)





class djikstra:
    
    def getneighbours(self, currentnode):
        neighbours = []
        neighbours.clear()
        weight = []
        weight.clear()
        returnnodes = []
        returnnodes.clear()
        nodes = {}
        infinity = float("inf")
        if currentnode[1] - 1 >= 0:
            topnode = (currentnode[0], currentnode[1] - 1)
            neighbours.append(topnode)
        if currentnode[1] + 1 < ROWS:
            bottomnode = (currentnode[0], currentnode[1] + 1)
            neighbours.append(bottomnode)
        if currentnode[0] - 1 >= 0:
            leftnode = (currentnode[0]-1, currentnode[1])
            neighbours.append(leftnode)
        if currentnode[0] + 1 < ROWS:
            rightnode = (currentnode[0]+1, currentnode[1])
            neighbours.append(rightnode)
        for neighbour in neighbours:
            weight.append(infinity)
        
        returnnodes.append(neighbours)
        
        nodes = [dict(zip(node,weight)) for node in returnnodes]

        
        return nodes
        #return topnode, bottomnode, leftnode, rightnode



    def checkdistance(self, node1, node2):
        x1, y1 = node1
        x2, y2 = node2

        if abs(x1-x2) + abs(y1-y2) == 1:
            return True
        else:
            return False  


    def algorithm(self, start, end, obstructions):
        #initialise
        unseennodes = {}
        graph = {}
        visited = {}
        graph.clear()
        visited.clear()
        unseennodes.clear()
        getneighbours = {}
        getneighbours.clear()
        track_path = []
        track_path.clear()
        obtainneighbours = []

        startnode = (start[0], start[1])
        endnode = (end[0], end[1])


        for row in range(ROWS):
            for col in range(ROWS):
                node = (row, col)
                getneighbours = self.getneighbours(node)
                unseennodes[node] = getneighbours
                graph[node] = getneighbours
        

        currentnode = startnode
        visited[currentnode] = 0 #set start node weight to 0

        if startnode == endnode: #if start and end node the same, print no path available on GUI
            return track_path

        try:
            while unseennodes:
                if currentnode == endnode:
                    break

                #get neighbours of current node
                obtainneighbours.clear()
                for neighbour in unseennodes[currentnode][0].items():
                    obtainneighbours.append(neighbour[0])

            
                
                #relax node weight of neighbours 
                for neighbour in obtainneighbours:
                    if neighbour not in visited and neighbour not in obstructions:
                        visited[neighbour] = visited[currentnode] + 1 #increment weight of neighbours with respect to current node 
                
                
                unseennodes.pop(currentnode)

                for node, weight in visited.items():
                    if node in unseennodes:
                        currentnode = node #get next nearest node for next iteration
                        break

        except KeyError:
            #print("no path possible")
            #problem occured when finding for neighbours as they are obstruction coordinates
            return track_path
        
        #get path
        #backtracking from end node to start node
        weight = visited[endnode]
        track_path.append(endnode)
        checknode = endnode
        temp = {}
        while weight != 0:
            weight = weight - 1
            temp.clear()
            for node in visited.keys():
                if visited[node] == weight:
                    temp[node] = weight
            for node in temp.keys():
                if self.checkdistance(node, checknode): #check if node to add is next nearest node to form path
                    track_path.append(node)
                    checknode = node
                    break
    
        return track_path


 


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pathfinding using Djikstra Algorithm')
g = GUI(screen)
d = djikstra()
p = Draw(screen)
path = []



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 0 <= x <= 600 and 0 <= y <= 600:
                    g.userinput(x, y)
                if 700 <= x <= 850 and 250 <= y <= 280:
                    g.clearUI()
                if 700 <= x <= 850 and 200 <= y <= 230:
                    path = d.algorithm(g.getstartnode(), g.getendnode(), g.getobstructions())
                    p.printpath(path)

    pygame.display.update()

        
    

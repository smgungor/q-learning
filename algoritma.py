import numpy as np
import pygame
import sys
import matplotlib.pyplot as plt
#sizes
screen_width = 1000
screen_heigth = 1000

gridsize = 20
grid_width = screen_width / gridsize
grid_height = screen_heigth / gridsize
size = 50

#colors
blue = (100,255,100)
red = (8, 182, 221)
block_color = (226, 16, 9)
agent_color = (255, 255, 0)



gamma = 0.75




lts = dict()
for i in range(0, size*size):
    key = str(i+1)
    lts[key] = i

rL = list()
sL = list()

neighborList = list()

def komsuGetir(cs):
  cs = cs+1
  neighborList.clear()
  i =int((cs-1)/size)
  j=int((cs-1)%size)

 

  if i==0 and j==0:
    neighborList.append(cs+size-1)
    neighborList.append(cs)
    neighborList.append(cs+size)
    return neighborList
    

  if i==0 and j==size-1:
    neighborList.append(cs+size-1)
    neighborList.append(cs-2)
    neighborList.append(cs+size-2)
    return neighborList

  if i==0 and (j>0 and j<size):
    neighborList.append(cs+size-1)
    neighborList.append(cs)
    neighborList.append(cs+size)
    neighborList.append(cs-2)
    neighborList.append(cs+size-2)
    return neighborList
    

  if i==size-1 and j==0:
    neighborList.append(cs-size-1)
    neighborList.append(cs)
    neighborList.append(cs-size)
    return neighborList
    

  if i==size-1 and j==size-1:
    neighborList.append(cs-size-1)
    neighborList.append(cs-2)
    neighborList.append(cs-size-2)
    return neighborList
       

  if i==size-1 and (j>0 and j<size):
    neighborList.append(cs-size-1)
    neighborList.append(cs)
    neighborList.append(cs-2)
    neighborList.append(cs-size-2)
    neighborList.append(cs-size)
    return neighborList
   

  if (i>0 and i<size) and j==0:
    neighborList.append(cs-size-1)
    neighborList.append(cs)
    neighborList.append(cs+size-1)
    neighborList.append(cs+size)
    neighborList.append(cs-size)
    return neighborList
    

  if (i>0 and i<size) and j==size-1:
    neighborList.append(cs-size-1)
    neighborList.append(cs+size-1)
    neighborList.append(cs-2)
    neighborList.append(cs-size-2)
    neighborList.append(cs+size-2)
    return neighborList
   
  
  else:
    neighborList.append(cs-size-1)
    neighborList.append(cs+size-1)
    neighborList.append(cs)
    neighborList.append(cs-2)
    neighborList.append(cs-size-2)
    neighborList.append(cs-size)
    neighborList.append(cs+size-2)
    neighborList.append(cs+size)
    return neighborList




mainTable = np.ones(size*size)
mainTable[:int(size*size*0.3)] = 0

np.random.shuffle(mainTable)
mainTable = (np.random.rand(size*size) > 0.3).astype(int)
mainTable = np.where(mainTable == 0, -5, mainTable)
mainTable = np.where(mainTable == 1, 3, mainTable)
mainTable = mainTable.reshape((size,size))

cMatrix = np.zeros((size*size,size*size), dtype=bool)



#sayısal kısmı string yapmak için kullanıldı
stl = dict((s, l)
                         for l, s in lts.items())



qTable = np.array(np.zeros([size*size, size*size]))


def findRoute(strtLoc, endLoc):
    stepCounter = 0
    totalP = 0
    
    
    endState = lts[endLoc]
    strtState = lts[strtLoc]
    

    mainTable[int(endState/size)][endState % size]=850
    

    mainTable[int(strtState/size)][strtState % size]=0
    
    blockWrite(mainTable)
    
    rTable = np.array(np.zeros([size*size, size*size]))
    
    for i in range(0, size):
        for j in range(0, size):
            if(i != size-1):
                rTable[i*size+j][(i+1)*size+j] = mainTable[i+1][j]  # down
            if(i != 0):
                rTable[i*size+j][(i-1)*size+j] = mainTable[i-1][j]  # up
            if(j != 0):
                rTable[i*size+j][i*size+(j-1)] = mainTable[i][j-1]  # left
            if(j != size-1):
                rTable[i*size+j][i*size+(j+1)] = mainTable[i][j+1]  # right
            if(j != size-1 and i != 0):
                rTable[i*size+j][(i-1)*size+(j+1)] = mainTable[i-1][j+1]  # up right
            if(j != 0 and i != 0):
                rTable[i*size+j][(i-1)*size+(j-1)] = mainTable[i-1][j-1]  # up left
            if(j != size-1 and i != size-1):
                rTable[i*size+j][(i+1)*size+(j+1)] = mainTable[i+1][j+1]  # down right
            if(j != 0 and i != size-1):
                rTable[i*size+j][(i+1)*size+(j-1)] = mainTable[i+1][j-1]  # down left
    rTableCopy = np.copy(rTable)
    
    
    
    
    
    curState = strtState
   
    
    for i in range(3000000):
        
        if (i%100000==0):
            print(i)
       
        
        
        
        
        pActions = []
        
        
                   
        for j in komsuGetir(curState):
          
          if rTableCopy[curState, j] != 0 and cMatrix[curState,j]!=True:
                pActions.append(j)
               
                
        
        
        nextState = np.random.choice(pActions)
       
       
        
        qTable[curState, nextState] = rTableCopy[curState,
                                                   nextState] + gamma * (qTable[nextState, np.argmax(qTable[nextState, ])])
       
        
        if rTableCopy[curState,nextState]==-5 or rTableCopy[curState,nextState]==850:
           
            if (rTableCopy[curState,nextState]==-5):

                cMatrix[:,nextState]=True
                totalP += -5
                
            
            else:
                totalP += 5

               
            
            stepCounter+=1
            sL.append(stepCounter)
            rL.append(totalP)
            curState=strtState
            stepCounter = 0
            totalP=0
            
                                       
        else:
            totalP+=3        
            curState= nextState
            stepCounter+=1
            
         
         
    
    route = [strtLoc]
    
    nextLoc = strtLoc
    
    
    while(nextLoc != endLoc):
        
        
        strtState = lts[strtLoc]
        

        nextState = np.argmax(qTable[strtState, ])
        

        nextLoc = stl[nextState]
        route.append(nextLoc)
        

        strtLoc = nextLoc

    return route


def blockWrite(nums):

    blockFile = open("engel.txt", "w")

    for i in range(size):
        for j in range(size):

            if nums[i, j] == -5:
                blockFile.write("("+str(i) + "," + str(j) + ",K" + ")\n")
            elif nums[i, j] == 0:
                blockFile.write("("+str(i) + "," + str(j) + ",M" + ")\n")
            elif nums[i, j] == 850:
                blockFile.write("("+str(i) + "," + str(j) + ",Y" + ")\n")
            else:
                blockFile.write("("+str(i) + "," + str(j) + ",B" + ")\n")

    blockFile.close()




def drawBoard(surface):
    global mainTable
    for i in range(0, size):
        for j in range(0, size):
            if mainTable[j, i] == 3:
                way = pygame.Rect(
                    (i * gridsize, j * gridsize,), (gridsize, gridsize))
                pygame.draw.rect(surface, red,
                                 way,)
            elif mainTable[j, i] == 850:
                finish = pygame.Rect(
                    (i * gridsize, j * gridsize,), (gridsize, gridsize))
                pygame.draw.rect(surface, blue,
                                 finish,)
            else:
                block = pygame.Rect(
                    (i * gridsize, j * gridsize,), (gridsize, gridsize))
                pygame.draw.rect(surface, block_color, block, 3)


class AGENT:
    def __init__(self, s_location):
        self.positions = [(s_location[1]*gridsize), (s_location[0]*gridsize)]
        self.length = 1

        self.color = agent_color
        self.score = 0

    def draw(self, surface):
        rect = pygame.Rect(
            (self.positions[0], self.positions[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, rect)

    def position_update(self, new_position, surface):
        self.positions = [(new_position[1]*gridsize), (new_position[0]*gridsize)]


def searchLocation(end_location):
    ending_state = lts[end_location]
    return (int(ending_state/size), ending_state % size)


def searchStartLocation(start_location):
    starting_state = lts[start_location]
    return (int(starting_state/size), starting_state % size)


def main(deger1,deger2):
    pygame.init()
    clock = pygame.time.Clock()
    global rL
    global sL
    yazi1 = str(deger1)
    yazi2 = str(deger2)
    print(yazi1 + ' ' + yazi2)
    optimal_route = findRoute(yazi1, yazi2)
    screen = pygame.display.set_mode((1000, 1000))
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawBoard(surface)
    firstAgent = AGENT(searchStartLocation(yazi1))
    bitisNoktasi = searchStartLocation(yazi2)
    
    fig ,axs = plt.subplots(2)
    plt.figure(figsize=(20,100))
    axs[0].plot(rL)
    axs[0].set_xlabel("Bölüm")
    axs[0].set_ylabel("Ödül")
    
    axs[1].plot(sL)
    axs[1].set_xlabel("Bölüm")
    axs[1].set_ylabel("Adım")
    
    axs[0].grid(True)
    axs[1].grid(True)
    
    firstAgent.draw(surface)
    sayac = 1
    while True:
        if sayac == len(optimal_route):
            pass
        else:
            firstAgent.position_update(
                searchLocation(optimal_route[sayac]), surface)
            firstAgent.draw(surface)
            sayac += 1
        clock.tick(2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(surface, (0, 0))

        pygame.display.update()
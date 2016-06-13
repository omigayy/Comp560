# Programmer: Jiabing Song, Yingying Wu
# Last Modified Date: 05/10/2015

from decimal import Decimal

grid = []
blueScore = 0
greenScore = 0
mmDepthLimit = 3
abDepthLimit = 4
iterationTime = 0
treeSet = []
INF = Decimal('-Infinity')     # used for max in alphaBeta
NINF = Decimal('Infinity')     # used for min in alphaBeta
abVisited = []
scoreLst = []

# ============= setup ============
def generateGrid():
   fileName = raw_input('Enter file name(with .txt):')
   gridFile = open(fileName,"r")
   global grid
   for line in gridFile:
      tmpArr = []
      tmpVal = [int(x) for x in line.split("\t")]
      for i in range(len(tmpVal)):
         tmpArr.append(GridCell(tmpVal[i]))
      grid.append(tmpArr)
def printGrid():
   for i in range(len(grid)):
      for j in range(len(grid[i])):
         print grid[i][j].value,
      print
class GridCell():
   def __init__(self, value):
      self.value = value
      self.color = None
def printColoredGrid():
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j].color == "blue":
                print "b",
            elif grid[i][j].color == "green":
                print "g",
            else:
                print "*",
        print
# ================================
# ============ actions ===========
# paint grid cell and add the score to a global score
def turnBlue(x,y):
   grid[x][y].color = "blue"
   global blueScore
   blueScore += grid[x][y].value
   captureG(x,y)
def turnGreen(x,y):
   grid[x][y].color = "green"
   global greenScore
   greenScore += grid[x][y].value
   captureB(x,y)
def captureG(x,y):
   adjSame = 0
   adjG = []
   if x > 0:
      if grid[x-1][y].color == "blue":
         adjSame = 1
      elif grid[x-1][y].color == "green":
         adjG.append([x-1,y])
   if y > 0:
      if grid[x][y-1].color == "blue":
         adjSame = 1
      elif grid[x][y-1].color == "green":
         adjG.append([x,y-1])
   if x < (len(grid)-1):
      if grid[x+1][y].color == "blue":
         adjSame = 1
      elif grid[x+1][y].color == "green":
         adjG.append([x+1,y])
   if y < (len(grid)-1):
      if grid[x][y+1].color == "blue":
         adjSame = 1
      elif grid[x][y+1].color == "green":
         adjG.append([x,y+1])
   if adjSame == 0:
      pass    # cannot capture
   elif len(adjG) == 0:
      pass    # nothing to capture
   else:   # w/ adjSame and adjG,start capture
      for i in range(len(adjG)):
         tmpx = adjG[i][0]
         tmpy = adjG[i][1]
         grid[tmpx][tmpy].color = "blue"
         global blueScore, greenScore
         blueScore += grid[tmpx][tmpy].value
         greenScore -= grid[tmpx][tmpy].value
def captureB(x,y):
   adjSame = 0
   adjB = []
   if x > 0:
      if grid[x-1][y].color == "green":
         adjSame = 1
      elif grid[x-1][y].color == "blue":
         adjB.append([x-1,y])
   if y > 0:
      if grid[x][y-1].color == "green":
         adjSame = 1
      elif grid[x][y-1].color == "blue":
         adjB.append([x,y-1])
   if x < (len(grid)-1):
      if grid[x+1][y].color == "green":
         adjSame = 1
      elif grid[x+1][y].color == "blue":
         adjB.append([x+1,y])
   if y < (len(grid)-1):
      if grid[x][y+1].color == "green":
         adjSame = 1
      elif grid[x][y+1].color == "blue":
         adjB.append([x,y+1])
   if adjSame == 0:
      pass    # cannot capture
   elif len(adjB) == 0:
      pass    # nothing to capture
   else:   # w/ adjSame and adjG,start capture
      for i in range(len(adjB)):
         tmpx = adjB[i][0]
         tmpy = adjB[i][1]
         grid[tmpx][tmpy].color = "green"
         global blueScore, greenScore
         greenScore += grid[tmpx][tmpy].value
         blueScore -= grid[tmpx][tmpy].value
# ================================

# =========== evaluation =========
# problem exist:
# didn't take moves in depth 1 and 2 into consideration
def evaluation(terminalNode):
    # update node.score
    h = 0
    i = 1
    j = 0
    score = h * terminalNode.score + i * evaluateToEat(terminalNode) + j * evaluateToBeEaten(terminalNode)
    if terminalNode.player == "max":
        terminalNode.score = score
    else:
        terminalNode.score = -score
def evaluateToEat(terminalNode):
    adjSame = 0
    adjG = []
    score = 0
    x = terminalNode.x
    y = terminalNode.y
    if terminalNode.player == "max":
        if x > 0:
            if grid[x - 1][y].color == "blue":
                adjSame = 1
            elif grid[x - 1][y].color == "green":
                adjG.append([x - 1, y])
        if y > 0:
            if grid[x][y - 1].color == "blue":
                adjSame = 1
            elif grid[x][y - 1].color == "green":
                adjG.append([x, y - 1])
        if x < (len(grid) - 1):
            if grid[x + 1][y].color == "blue":
                adjSame = 1
            elif grid[x + 1][y].color == "green":
                adjG.append([x + 1, y])
        if y < (len(grid) - 1):
            if grid[x][y + 1].color == "blue":
                adjSame = 1
            elif grid[x][y + 1].color == "green":
                adjG.append([x, y + 1])
        if adjSame == 0:
            return 0  # cannot capture
        elif len(adjG) == 0:
            return 0  # nothing to capture
        else:  # w/ adjSame and adjG,start capture
            for i in range(len(adjG)):
                tmpx = adjG[i][0]
                tmpy = adjG[i][1]
                score += grid[tmpx][tmpy].value
    elif terminalNode.player == "min":
        if x > 0:
            if grid[x - 1][y].color == "green":
                adjSame = 1
            elif grid[x - 1][y].color == "blue":
                adjG.append([x - 1, y])
        if y > 0:
            if grid[x][y - 1].color == "green":
                adjSame = 1
            elif grid[x][y - 1].color == "blue":
                adjG.append([x, y - 1])
        if x < (len(grid) - 1):
            if grid[x + 1][y].color == "green":
                adjSame = 1
            elif grid[x + 1][y].color == "blue":
                adjG.append([x + 1, y])
        if y < (len(grid) - 1):
            if grid[x][y + 1].color == "green":
                adjSame = 1
            elif grid[x][y + 1].color == "blue":
                adjG.append([x, y + 1])
        if adjSame == 0:
            return 0  # cannot capture
        elif len(adjG) == 0:
            return 0  # nothing to capture
        else:  # w/ adjSame and adjG,start capture
            for i in range(len(adjG)):
                tmpx = adjG[i][0]
                tmpy = adjG[i][1]
                score += grid[tmpx][tmpy].value
    return score*2
def evaluateToBeEaten(terminalNode):
    x = terminalNode.x
    y = terminalNode.y
    score = 0
    canBeEaten = 0
    if terminalNode.player == "max":
        opposite = "green"
    else:
        opposite = "blue"
    if x < (len(grid) - 1) and y < (len(grid) - 1):
        if grid[x+1][y+1] == opposite:
            canBeEaten = 1
    elif x < (len(grid) - 1) and y > 1:
        if grid[x + 1][y - 1] == opposite:
            canBeEaten = 1
    elif x > 1 and y < (len(grid) - 1):
        if grid[x - 1][y + 1] == opposite:
            canBeEaten = 1
    elif x > 1 and y > 1:
        if grid[x - 1][y - 1] == opposite:
            canBeEaten = 1
    elif x < (len(grid) - 2):
        if grid[x+2][y] == opposite:
            canBeEaten = 1
    elif x > 2:
        if grid[x - 2][y] == opposite:
            canBeEaten = 1
    elif y < (len(grid)) - 2:
        if grid[x][y+2] == opposite:
            canBeEaten = 1
    elif y > 2:
        if grid[x][y-2] == opposite:
            canBeEaten = 1
    if canBeEaten == 1:
        score = 0 - terminalNode.value * 2
    return score
# ================================

class MmNode():
#contains coordinate, max/min, score(utility)
   def __init__(self,x,y):
      self.x = x
      self.y = y
      self.player = None
      self.score = 0
# ========= minimax recursion ========
# return optimal choice(a mmNode) for a
def miniMax(player):
    availGrids = []
    global iterationTime
    iterationTime = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j].color == None:
                availGrids.append(MmNode(i,j))
   
    if player == "max":
        iterationTime += 1
        maxNode = MmNode(0,0)
        maxNode = mmMin(availGrids,availGrids[0])
        for i in range(1,len(availGrids)):
            tmp = mmMin(availGrids,availGrids[i])
            if tmp.score > maxNode.score:
                maxNode = tmp
        return maxNode
        # for i in range(l)en(availGrids)):
        #     max(availGrids,availGrids[i]
    elif player == "min":
        iterationTime += 1
        minNode = mmMax(availGrids,availGrids[0])
        for i in range(1,len(availGrids)):
            tmp = mmMax(availGrids,availGrids[i])
            if tmp.score < minNode.score:
                minNode = tmp
        return minNode
        # for i in range(len(availGrids)):
        #     min(availGrids,availGrids[i])
def mmMax(availGrids,mmNode):
# return the node w/ max value
    global iterationTime, mmDepthLimit
    iterationTime += 1

    if gameOver(mmNode):
        evaluation(mmNode)
        return mmNode

    if iterationTime >= mmDepthLimit:
        mmNode.player = "max"
        evaluation(mmNode)
        iterationTime -= 1
        return mmNode

    else:
        availGrids.remove(mmNode)
        maxNode = mmMin(availGrids,availGrids[0])
        for i in range(1,len(availGrids)):
            tmp = mmMin(availGrids,availGrids[i])
            if tmp.score > maxNode.score:
                maxNode = tmp
        return maxNode
def mmMin(availGrids,mmNode):
# return the node w/ min value
    global iterationTime, mmDepthLimit
    iterationTime += 1

    if gameOver(mmNode):
        evaluation(mmNode)
        return mmNode

    if iterationTime >= mmDepthLimit:
    # if reach depth limit
        mmNode.player = "min"
        evaluation(mmNode)
        iterationTime -= 1
        return mmNode
        # min = availGrids[0]
        # evaluation(min)
        # for i in range(1,len(availGrids)):
        #     evaluation(availGrids[i])
        #     if availGrids[i].score < min.score:
        #         min = availGrids[i]
        # iterationTime -= 1
        # return min

    else:
        availGrids.remove(mmNode)
        minNode = mmMax(availGrids,availGrids[0])
        for i in range(1,len(availGrids)):
            tmp = mmMax(availGrids,availGrids[i])
            if tmp.score < minNode.score:
                minNode = tmp
        return minNode
# ====================================

def gameOver(mmNode):
# detect if it will gameOver after a move, return 1 if gameover
   fullGrid = 1
   if grid[mmNode.x][mmNode.y].color == None:
      grid[mmNode.x][mmNode.y].color = "tmpColor"
   for i in range(len(grid)):
      for j in range(len(grid[i])):
         if grid[i][j].color == None:
            fullGrid = 0
   grid[mmNode.x][mmNode.y].color = None
   return fullGrid
def gameOverGrid():
#return 1 if gameover
   fullGrid = 1
   for i in range(len(grid)):
      for j in range(len(grid[i])):
         if grid[i][j].color == None:
            fullGrid = 0
   return fullGrid

class AbNode():
#contains coordinate, max/min, score(utility)
    def __init__(self,x,y,player):
        self.x = x
        self.y = y
        self.player = player
        self.score = 0
        self.alpha = 0
        self.beta = 0

def findSuccessor(abNode):
    successor = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j].color == None and ([i,j]not in abVisited):
                if abNode.player == "max":
                    successor.append(AbNode(i,j,"min"))
                else:
                    successor.append(AbNode(i,j,"max"))
    return successor

def alphaBeta(player):
    # return a node w/ x, y
    root = AbNode(None,None,player)
    global iterationTime,scoreLst
    iterationTime = 0
    score = alphaBetaRecur(root,NINF,INF)
    if player == "max":
        maxIndex = 0
        for i in range(len(scoreLst)):
            if scoreLst[i].score > scoreLst[maxIndex].score:
                maxIndex = i
        return scoreLst[maxIndex]
    elif player == "min":
        minIndex = 0
        for i in range(len(scoreLst)):
            if scoreLst[i].score < scoreLst[minIndex].score:
                minIndex = i
        return scoreLst[minIndex]

def alphaBetaRecur(abNode,A,B):  # A always less than B
    global abVisited, scoreLst
    abVisited.append([abNode.x,abNode.y])
    global iterationTime
    iterationTime += 1
    if iterationTime > abDepthLimit: # N is a leaf
        evaluation(abNode)
        iterationTime -= 1
        abVisited.pop()
        return abNode.score

    else:
        abNode.alpha = NINF
        abNode.beta = INF
        if abNode.player == "min":
            successor = findSuccessor(abNode)
            for child in successor:
                child.score = alphaBetaRecur(child,A,min(B, abNode.beta))
                abNode.beta = min(abNode.beta,child.score)  # child.score or abNode.score?
                if A >= abNode.beta:        # decide whether can prune
                    abVisited.pop()
                    scoreLst.append(abNode)
                    return abNode.beta
            abVisited.pop()
            scoreLst.append(abNode)
            return abNode.beta
        
        elif abNode.player == "max":
            successor = findSuccessor(abNode)
            for child in successor:
                child.score = alphaBetaRecur(child,max(A,abNode.alpha),B)
                abNode.alpha = max(abNode.alpha,child.score)  # child.score or abNode.score?
                if abNode.alpha >= B:
                    abVisited.pop()     # according to my genius math instinct
                    scoreLst.append(abNode)
                    return abNode.alpha
            abVisited.pop()
            scoreLst.append(abNode)
            return abNode.alpha
            
def main():
    generateGrid()
    printGrid()
    while (not gameOverGrid()):
        blue = miniMax("max")
        x,y = blue.x, blue.y
        print "blue: ", x, y
        turnBlue(x,y)
        green = miniMax("min")
        x,y = green.x, green.y
        print "green: ", x, y
        turnGreen(x,y)


    print "========================="
    printColoredGrid()
    print blueScore
    print greenScore

    if blueScore > greenScore:
        print "Blue wins!"
    elif greenScore > blueScore:
        print "Green wins!"
    else:
        print "It's a tie"

if __name__ == '__main__':
   main()
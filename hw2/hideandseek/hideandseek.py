__author__ = 'inkhk'
# Programmer: Jiabing Song, Yingying Wu
# Last Modified Date: 10/10/2015
# TODO: fileName change back to keyboard input

from random import randint

numFriends = 0
numTrees = 0
friends = []
iteration = 0

class Friend():
   def __init__(self, x,y):
       self.x = x
       self.y = y
       self.constraint = []

def generateForest():
  #fileName = raw_input('Enter file name(with .txt):')
  fileName = "input5.txt"
  treeFile = open(fileName,"r")
  global numTrees,numFriends
  numFriends,numTrees = [int(x) for x in treeFile.readline().split()]
  forest = []
  for i in range (numFriends):
      new = []
      for j in range (numFriends):
          new.append(" ")
      forest.append(new)
  for line in treeFile:
      x,y = [int(x) for x in line.split()]
      forest[x-1][y-1] = "T"
  return forest

def putFriends(forest,numFriends):
  for i in range (numFriends):
      t = randint(0,numFriends-1)
      while (forest[t][i] == "T"):
              t = randint(0,numFriends-1)
      forest[t][i] = "F"
      friends.append(Friend(t,i))

def findConstraints(friend,forest):
    friend.constraint = []
    length = len(forest)
    #left(x)
    i = friend.y - 1
    while(i >= 0):
        if(forest[friend.x][i] == "T"):
            break
        if(forest[friend.x][i] == "F"):
            friend.constraint.append([friend.x,i])
            break
        i -= 1
    #right(x)
    i = friend.y + 1
    while(i < length):
        if(forest[friend.x][i] == "T"):
            break
        if(forest[friend.x][i] == "F"):
            friend.constraint.append([friend.x,i])
            break
        i += 1
    #up(x)
    i = friend.x - 1
    while(i >= 0):
        if(forest[i][friend.y] == "T"):
            break
        if(forest[i][friend.y] == "F"):
            friend.constraint.append([i,friend.y])
            break
        i -= 1
    #down(x)
    i = friend.x + 1
    while(i < length):
        if(forest[i][friend.y] == "T"):
            break
        if(forest[i][friend.y] == "F"):
            friend.constraint.append([i,friend.y])
            break
        i += 1
    #upper-left(x)
    i = friend.x - 1
    j = friend.y - 1
    while (i >= 0 and j >= 0):
        if(forest[i][j] == "T"):
            break
        if(forest[i][j] == "F"):
            friend.constraint.append([i,j])
            break
        i -= 1
        j -= 1
    #upper-right(x)
    i = friend.x - 1
    j = friend.y + 1
    while (i >= 0 and j < length):
        if(forest[i][j] == "T"):
            break
        if(forest[i][j] == "F"):
            friend.constraint.append([i,j])
            break
        i -= 1
        j += 1

    #lower-left(x)
    i = friend.x + 1
    j = friend.y - 1
    while ( i < length and j >= 0 ):
        if(forest[i][j] == "T"):
            break
        if(forest[i][j] == "F"):
            friend.constraint.append([i,j])
            break
        i += 1
        j -= 1
    #lower-right(x)
    i = friend.x + 1
    j = friend.y + 1
    while ( i < length and j < length ):
        if(forest[i][j] == "T"):
            break
        if(forest[i][j] == "F"):
            friend.constraint.append([i,j])
            break
        i += 1
        j += 1

def findAllConstraints(friends,forest):
    for i in range(len(friends)):
        findConstraints(friends[i],forest)

def findMostConstrained(friends):
    # returns the index of the most constrained friend in friends list
    mostConstrained = 0
    for i in range(len(friends)):
        if len(friends[i].constraint) > len(friends[mostConstrained].constraint):
            mostConstrained = i
    return mostConstrained

def improveSingle(friend,forest):
    thisY = friend.y
    leastCon = len(friend.constraint)
    forest[friend.x][thisY] = " "
    leastX = friend.x
    for i in range(numFriends):
        if forest[i][thisY] != "T":
            tmpfriend = Friend(i,thisY)
            findConstraints(tmpfriend,forest)
            if len(tmpfriend.constraint) < leastCon:
                leastCon = len(tmpfriend.constraint)
                leastX = tmpfriend.x
    forest[leastX][thisY] = "F"
    friend.x = leastX


def improveMostConstrained(friends,forest):
    index = findMostConstrained(friends)
    #print "most contraint:",index
    improveSingle(friends[index],forest)
    #print friends[index].x,friends[index].y

def findTotalCon(friends,forest):
# update friend's constrain to its class
# and return number total constraints
    totalCon = 0
    findAllConstraints(friends,forest)
    for i in range(numFriends):
        totalCon += len(friends[i].constraint)
    return totalCon

def randomStart(forest):
    rnd = randint(0,numFriends-1)
    improveSingle(friends[rnd],forest)


def improveAll(friends,forest):
    totalCon = findTotalCon(friends,forest)
    canMove = 1
    while canMove:
        global iteration
        iteration += 1
        improveMostConstrained(friends,forest)
        newTotalCon = findTotalCon(friends,forest)
        if newTotalCon == 0:    #improve to best
            break
        change = totalCon - newTotalCon
        if change == 0:     #cannot improve the most constrained one
            randomStart(forest)
        totalCon = newTotalCon
        if allStuck(forest):
            randomMove(forest)


def singleStuck(friend,forest):
    # return 1 if stuck
    thisY = friend.y
    thisCon = len(friend.constraint)
    for i in range (numFriends):
        if (forest[i][thisY] != "T"):
            tmpfriend = Friend(i,thisY)
            findConstraints(tmpfriend,forest)
            if len(tmpfriend.constraint) < thisCon:
                return 0
    return 1

def allStuck(forest):
    # return 1 if all friend stuck
    for i in range(numFriends):
        if singleStuck(friends[i],forest) == 0:
            #print "not stuck at friends: ",i
            return 0
    return 1

def randomMove(forest):
    # randomly step back/
    rnd = randint(0,numFriends-1)
    rndx = randint(0,numFriends-1)
    while forest[rndx][friends[rnd].y] == "T" or forest[rndx][friends[rnd].y] == "F" :
        rndx = randint(0,numFriends-1)
    forest[friends[rnd].x][friends[rnd].y] = " "
    forest[rndx][friends[rnd].y] = "F"
    friends[rnd].x = rndx
    #print "I move!"

def printConstraint(friends):
    for i in range (numFriends):
        print "Constraints of " , friends[i].x, friends[i].y , ":"
        for j in range(len(friends[i].constraint)):
            print friends[i].constraint[j],
            print

def printForest(forest):
    for i in range(len(forest)):
        for j in range(len(forest[i])):
            print forest[i][j],
        print


def main():
    forest = generateForest()
    print numFriends, numTrees
    putFriends(forest,numFriends)
    printForest(forest)
    # for i in range(numFriends-1):
    #     print friends[i].x, friends[i].y
    findAllConstraints(friends,forest)
    printConstraint(friends)
    # i = findMostConstrained(friends)
    print "==================================================="
    improveAll(friends,forest)
    printForest(forest)
    findAllConstraints(friends,forest)
    printConstraint(friends)
    print "iteration:", iteration
if __name__ == '__main__':
  main()





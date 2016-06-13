#============ver 0909 19:22==========
# Programmer: Jiabing Song, Yingying Wu
# Date last modified: 09/09/2015, 2:11
# Status: finished

# ========  keep track of steps   ==========
path_cost = 0   # number of steps from S to G of the solution
node_cost = 0   # number of nodes expanded
explored_set = [] # a set used to indicate where we have been
frontier_set = [] # a set of frontiers; used in BFS, A*

# ===== read maze file into a 2D array =====
def readMaze():
  maze = []
  fileName = raw_input('Enter file name(with .txt):')
  mazeFile = open(fileName,"r")
  for line in mazeFile:
      maze.append(list(line))
  mazeFile.close()
  return maze

# ======= declare a class storing state ======
class State(object):
  def __init__(self,right,down,left,up):
      self.right = right
      self.down = down
      self.left = left
      self.up = up

# ==========  set starting place   ============
def starting_place(maze):
    # find "S" and return its coordinate
  for i in range(len(maze)):
      for j in range(len(maze[i])):
          if maze[i][j] == "S":
              explored_set.append([i,j])
              return i,j

# ========  look around check state   ==========
def check_current_state(maze,place):
    # if it's a wall or it has been explored, set it to false to represent should not go
  current_state = State(1,1,1,1)

  if maze[place[0]][place[1] + 1] == "%" or (([place[0],place[1] + 1]) in explored_set):
      current_state.right = 0
  if maze[place[0] + 1][place[1]] == "%" or (([place[0] + 1,place[1]]) in explored_set):
      current_state.down = 0
  if maze[place[0]][place[1] - 1] == "%" or (([place[0],place[1] - 1]) in explored_set):
      current_state.left = 0
  if maze[place[0] - 1][place[1]] == "%" or (([place[0] - 1,place[1]]) in explored_set):
      current_state.up = 0

  return current_state

# =================  action   ===================
    #return a changed coordinate and add the new coordinate into the explored set
def go_right(place):
  place = [place[0],place[1]+1]
  explored_set.append(place)
  return place
def go_down(place):
  place = [place[0]+1,place[1]]
  explored_set.append(place)
  return place
def go_left(place):
  place = [place[0],place[1]-1]
  explored_set.append(place)
  return place
def go_up(place):
  place = [place[0]-1,place[1]]
  explored_set.append(place)
  return place

# ================  dfs tree   ==================

def dfs_initiate_tree(start_place):
    # initiate a tree for dfs
    # set the starting place as root
    # use a LIFO data structure to represent the tree
  stack = []
  stack.append(start_place)
  global node_cost
  node_cost += 1
  return stack

def dfs_add_node(stack, new_place):
  stack.append(new_place)
  global node_cost
  node_cost += 1

def dfs_go_back(stack,place):
  stack.pop()
  place = stack[-1]
  return place

def dfs_mark_dots(maze,stack):
    # mark the final path to the goal and count the path cost
  global path_cost
  path_cost += 1
  stack.pop()
  while len(stack)!= 1:
      buff = stack.pop()
      maze[buff[0]][buff[1]] = "."
      path_cost += 1

# ===================== BFS =====================
class BFS_node(object):
   def __init__(self,parent,place):
       self.parent = parent
       self.place = place
       self.total_dist = 0
def bfs_initiate_tree(start_place):
 root = BFS_node(None,start_place)
 frontier_set.append(root)
 global node_cost
 node_cost += 1
 return root

# ===============  BFS action   =================
def bfs_right(node):
  child = BFS_node(node,go_right(node.place))
  frontier_set.append(child)
  global node_cost
  node_cost += 1
def bfs_down(node):
  child = BFS_node(node,go_down(node.place))
  frontier_set.append(child)
  global node_cost
  node_cost += 1
def bfs_left(node):
  child = BFS_node(node,go_left(node.place))
  frontier_set.append(child)
  global node_cost
  node_cost += 1
def bfs_up(node):
  child = BFS_node(node,go_up(node.place))
  frontier_set.append(child)
  global node_cost
  node_cost += 1

def bfs_defront(maze,frontier_set):
  state = check_current_state(maze,frontier_set[0].place)
  if state.right == state.down == state.left == state.up == 0:
      frontier_set.pop(0)

def bfs_mark_dots(maze,queue):
  buffer = queue.pop()
  global path_cost
  path_cost += 1
  while buffer.parent.parent != None:
      maze[buffer.parent.place[0]][buffer.parent.place[1]] = "."
      buffer = buffer.parent
      path_cost += 1

# ===============  greedy best  =================

def find_goal(maze):
  for i in range(len(maze)):
      for j in range(len(maze[i])):
          if maze[i][j] == "G":
              return i,j

def distance(goal,place):
  dis = abs(goal[0]-place[0]) + abs(goal[1]-place[1])
  return dis

def find_smallest(maze,goal,place):  # return the coordinate of the place we should go to
# this is the stupidest function I've ever written...
  state = check_current_state(maze,place)
  if state.right:
      dis_r = distance(goal,[place[0],place[1]+1])
  else:
      dis_r = "a"
  if state.down:
      dis_d = distance(goal,[place[0] + 1,place[1]])
  else:
      dis_d = "a"
  if state.left:
      dis_l = distance(goal,[place[0],place[1]-1])
  else:
      dis_l = "a"
  if state.up:
      dis_u = distance(goal,[place[0] - 1,place[1]])
  else:
      dis_u = "a"
  dis_arr = [dis_r,dis_d,dis_l,dis_u]
  if min(dis_arr) != "a":
      smallest = dis_arr.index(min(dis_arr)) # in main, eliminate the dead end case
  if smallest == 0:
      place = go_right(place)
  elif smallest == 1:
      place = go_down(place)
  elif smallest == 2:
      place = go_left(place)
  elif smallest == 3:
      place = go_up(place)

  return place

# ===============  A *  =================
def current_path_cost(node):
   current_path_cost = 0
   while node.parent != None:
      node = node.parent
      current_path_cost += 1
   return current_path_cost

def sort_frontier(goal,frontier_set):
   for node in frontier_set:
       node.total_dist = distance(goal,node.place) + current_path_cost(node)
       # print node.total_dist
   sorted_set = sorted(frontier_set, key=lambda x: x.total_dist, reverse=False)
   # for i in range(len(sorted_set)):
   #         print sorted_set[i].place,
   # print ""
   return sorted_set


# ===========  if it is the goal   =============
def check_goal(maze,place):
  if maze[place[0]][place[1]] == "G":
      return True

# ==============  print maze   ================
def print_maze(maze):
  for i in range(len(maze)):
      for j in range(len(maze[i])):
          print maze[i][j],

# ===========================================


def main():
    maze = readMaze()
    start = [0,0]
    start[0],start[1] = starting_place(maze) # decide staring place
    place = start

    search_method = raw_input("Which search method do you want to use(dfs/bfs/greedybest/a* in lower case):")

# ======================== dfs ===========================
    if search_method == "dfs":
        dfs_stack = dfs_initiate_tree(place)
        state = State(1,1,1,1)

        while not check_goal(maze,place):
            state = check_current_state(maze, place)
            if state.right:
                place = go_right(place)
                dfs_add_node(dfs_stack,place)
            elif state.down:
                place = go_down(place)
                dfs_add_node(dfs_stack,place)
            elif state.left:
                place = go_left(place)
                dfs_add_node(dfs_stack,place)
            elif state.up:
                place = go_up(place)
                dfs_add_node(dfs_stack,place)
            else:
                place = dfs_go_back(dfs_stack,place)
        dfs_mark_dots(maze,dfs_stack)
        print_maze(maze)
        print "path cost: " + str(path_cost)
        print "node cost: " + str(node_cost)

# ======================= bfs ===========================
    elif search_method == "bfs":
        root = bfs_initiate_tree(place)
        current_node = root

        while 1:
            buffer_state = check_current_state(maze,current_node.place)
            if buffer_state.right:
                if not check_goal(maze,[current_node.place[0],current_node.place[1] + 1]):
                    bfs_right(current_node)
                else:
                    bfs_right(current_node)
                    break
            if buffer_state.down:
                if not check_goal(maze,[current_node.place[0] + 1,current_node.place[1]]):
                    bfs_down(current_node)
                else:
                    bfs_down(current_node)
                    break
            if buffer_state.left:
                if not check_goal(maze,[current_node.place[0],current_node.place[1] - 1]):
                    bfs_left(current_node)
                else:
                    bfs_left(current_node)
                    break
            if buffer_state.up:
                if not check_goal(maze,[current_node.place[0] - 1,current_node.place[1]]):
                    bfs_up(current_node)
                else:
                    bfs_up(current_node)
                    break
            bfs_defront(maze,frontier_set)
            current_node = frontier_set[0]
        bfs_mark_dots(maze,frontier_set)
        print_maze(maze)
        print "path cost: " + str(path_cost)
        print "node cost: " + str(node_cost)

# ===================== greedy best ========================
    elif search_method == "greedybest":
        greedy_stack = dfs_initiate_tree(place)
        state = State(1,1,1,1)
        goal = [0,0]
        goal[0],goal[1] = find_goal(maze)

        while not check_goal(maze,place):
            state = check_current_state(maze, place)
            if (state.up + state.left + state.down + state.right) != 0:
                place = find_smallest(maze,goal,place)
                dfs_add_node(greedy_stack,place)
            else:
                place = dfs_go_back(greedy_stack,place)
        dfs_mark_dots(maze,greedy_stack)
        print_maze(maze)
        print "path cost: " + str(path_cost)
        print "node cost: " + str(node_cost)

# ===================== A * ========================
    elif search_method == "a*":
        root = bfs_initiate_tree(place)
        current_node = root
        goal = [0,0]
        goal[0],goal[1] = find_goal(maze)

        while 1:
            buffer_state = check_current_state(maze,current_node.place)
            if buffer_state.right:
                if not check_goal(maze,[current_node.place[0],current_node.place[1] + 1]):
                    bfs_right(current_node)
                else:
                    bfs_right(current_node)
                    break
            if buffer_state.down:
                if not check_goal(maze,[current_node.place[0] + 1,current_node.place[1]]):
                    bfs_down(current_node)
                else:
                    bfs_down(current_node)
                    break
            if buffer_state.left:
                if not check_goal(maze,[current_node.place[0],current_node.place[1] - 1]):
                    bfs_left(current_node)
                else:
                    bfs_left(current_node)
                    break
            if buffer_state.up:
                if not check_goal(maze,[current_node.place[0] - 1,current_node.place[1]]):
                    bfs_up(current_node)
                else:
                    bfs_up(current_node)
                    break

            global frontier_set
            bfs_defront(maze,frontier_set)
            frontier_set = sort_frontier(goal,frontier_set)

            current_node = frontier_set[0]
        bfs_mark_dots(maze,frontier_set)
        print_maze(maze)
        print "path cost: " + str(path_cost)
        print "node cost: " + str(node_cost)

    else:
        print "Error: check your input method name and retry"


if __name__ == "__main__":
  main()



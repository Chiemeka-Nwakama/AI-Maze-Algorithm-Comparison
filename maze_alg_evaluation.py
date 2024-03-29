import contextlib
import random

import random
import threading

import time

import os

import sys
import maze_alg_evaluation


import threading
import time
maze_alg_evaluation.doc_name = ""
maze_alg_evaluation.file = None

class MyThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            print("Thread is running...")
            time.sleep(1)

    def stop(self):
        self._stop_event.set()

class maze:

    '''
    The state will be a dictionary where the key is a integer pair and the value is information about 
    the cell's walls 

    An integer pair is represented as a tuple.
    Information about walls is saved as a list with elements being strings. 
    Example: 
        (1,2) : ["U", "D"]    # at (1,2) there is a wall above and bellow the cell. 
    '''

    '''
    Initialize the class. 

    state: A dictionary with integer pairs as the key and information about walls as the value.
    loc: A integer pair about where the agent.
    goal: A integer pair about where the agent wants to go.
    '''
    def __init__(self, environment, goal, loc = (0,0), width = 2, height = 2):
        self.environment = environment
        self.loc = loc
        self.goal = goal
        self.results = dict()
        self.untried = dict()
        self.unbacktracked = dict()
        
        self.width = width
        self.height = height
        self.time = 0
        self.end_time = 0

    
    def make_list(self, loc, goal):
        X_dir = goal[0] - loc[0]
        Y_dir = goal[1] - loc[1]
        full = ['U', 'D', 'R', 'L']
        ret_list = []
        
        if (abs(X_dir) >= abs(Y_dir)):
            if X_dir > 0:
                ret_list.append('U')
            else:
                ret_list.append('D')
            if Y_dir > 0:
                ret_list.append('R')
            else:
                ret_list.append('L')
            # print(ret_list) # Used to debug
            return ret_list + list(set(full) - set(ret_list))

        if (abs(X_dir) < abs(Y_dir)):
            if X_dir > 0:
                ret_list.append('U')
            else:
                ret_list.append('D')
            if Y_dir > 0:
                ret_list.append('R')
            else:
                ret_list.append('L')
            # print(ret_list) # Used to debug
            return ret_list + list(set(full) - set(ret_list))
        
    

    def possible_actions_unDir(self, loc):
        walls = self.loc
        actions = ['U', 'D', 'R', 'L'] # TODO: randomize this line
        if loc[1] == 0:
            with contextlib.suppress(ValueError):
                actions.remove('D')
        if loc[0] == 0:
            with contextlib.suppress(ValueError):
                actions.remove('L')
        if loc[1] == self.height:
            with contextlib.suppress(ValueError):
                actions.remove('U')
        if loc[0] == self.width:
            with contextlib.suppress(ValueError):
                actions.remove('R')
        for x in walls:
            with contextlib.suppress(ValueError):
                actions.remove(x)
        return actions
    
    def possible_actions_Dir(self, loc):
        walls = self.loc
        actions = self.make_list(self.loc, self.goal)
        if loc[1] == 0:
            with contextlib.suppress(ValueError):
                actions.remove('D')
        if loc[0] == 0:
            with contextlib.suppress(ValueError):
                actions.remove('L')
        if loc[1] == self.height:
            with contextlib.suppress(ValueError):
                actions.remove('U')
        if loc[0] == self.width:
            with contextlib.suppress(ValueError):
                actions.remove('R')
        for x in walls:
            with contextlib.suppress(ValueError):
                actions.remove(x)
        return actions

    def result(self, action):
        if action == 'R':
            self.loc =  (self.loc[0] + 1, self.loc[1])
        elif action == 'L':
            self.loc =  (self.loc[0] - 1, self.loc[1])
        elif action == 'U':
            self.loc =  (self.loc[0], self.loc[1] + 1)
        elif action == 'D':
            self.loc = (self.loc[0], self.loc[1] - 1)
        return self.loc
    
    def test_result(self, action, curr):
        if action == 'R':
            curr =  (curr[0] + 1, curr[1])
        elif action == 'L':
            curr =  (curr[0] - 1, curr[1])
        elif action == 'U':
            curr =  (curr[0], curr[1] + 1)
        elif action == 'D':
            curr = (curr[0], curr[1] - 1)
        return curr
    
    def isGoal(self):
        return self.loc == self.goal
    
    def find_back_action(self, temp, curr):
        for action in ['U', 'D', 'L', 'R']:
            if self.test_result(action, curr) == temp:
                return action
    
    def solveDir(self):
        beg_time = time.time()
        a = None
        s_prev = None
        s_curr = self.loc
        actions_taken = []


        while True:
            a = self.online_dfs_Agent_Dir(s_curr, s_prev, a)
            self.end_time = time.time()
            if a == None: break
            s_prev = s_curr
            s_curr = self.result(a)
            actions_taken.append(a)
            # print("Loc: ", self.loc, "Action: ", a) # Used to debug
        print("actions_taken ==", actions_taken)
        end_time = time.time()
        return (actions_taken, (end_time - beg_time))

    def online_dfs_Agent_Dir(self, s_curr, s_prev, a):
        
        if self.isGoal() == True: return None
        if s_curr not in self.untried:
            self.untried.update({s_curr: self.possible_actions_Dir(s_curr)})
        if s_prev != None:
            self.results.update({s_curr: (s_prev, a)})
            if s_curr in self.unbacktracked:
                self.unbacktracked[s_curr].append(s_prev)
            else:
                self.unbacktracked.update({s_curr: [s_prev]})
        if not self.untried[s_curr]: # returns True if list is empty
            if not self.unbacktracked[s_curr]: return None
            else:
                # print("Unbacktracked: ", self.unbacktracked, "Loc: ", self.loc) # Used to debug
                temp = self.unbacktracked[s_curr].pop()
                a = self.find_back_action(temp, s_curr)
                # print("Action: ", a) # Used to debug
        else:
            a = self.untried[s_curr].pop(0)
        return a

    def solve(self):
        beg_time = time.time()
        a = None
        s_prev = None
        s_curr = self.loc
        actions_taken = []
        self.time = time.time()
        while True:
            a = self.online_dfs_Agent(s_curr, s_prev, a)
            if a == None: break
            s_prev = s_curr
            s_curr = self.result(a)
            actions_taken.append(a)
            # print("Loc: ", self.loc, "Action: ", a) # Used to debug
        print("actions_taken ==", actions_taken)
        end_time = time.time()
        return (actions_taken, (end_time - beg_time))

    def online_dfs_Agent(self, s_curr, s_prev, a):
        if self.isGoal() == True: return None
        if s_curr not in self.untried:
            self.untried.update({s_curr: self.possible_actions_unDir(s_curr)})
        if s_prev != None:
            self.results.update({s_curr: (s_prev, a)})
            if s_curr in self.unbacktracked:
                self.unbacktracked[s_curr].append(s_prev)
            else:
                self.unbacktracked.update({s_curr: [s_prev]})
        if not self.untried[s_curr]: # returns True if list is empty
            if not self.unbacktracked[s_curr]: return None
            else:
                # print("Unbacktracked: ", self.unbacktracked, "Loc: ", self.loc) # Used to debug
                temp = self.unbacktracked[s_curr].pop()
                a = self.find_back_action(temp, s_curr)
                # print("Action: ", a) # Used to debug
        else:
            a = self.untried[s_curr].pop(0)
        return a




def generate_maze(width, height):
    
  
    maze = {(x, y): [] for x in range(width) for y in range(height)}

    def carve_path(x, y):
        directions = [(2, 0, 'R'), (-2, 0, 'L'), (0, 2, 'D'), (0, -2, 'U')]
        random.shuffle(directions)

        for dx, dy, direction in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < width and 0 <= ny < height and not maze[(nx, ny)]:
                maze[(x, y)].append(direction)
                maze[(nx, ny)].append(get_opposite_direction(direction))
                carve_path(nx, ny)

    def get_opposite_direction(direction):
        opposites = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}
        return opposites[direction]

    start_x, start_y = random.randrange(0, width, 2), random.randrange(0, height, 2)
    goal_x, goal_y = random.randrange(0, width, 2), random.randrange(0, height, 2)

    # Mark the starting and goal positions
    maze[(start_x, start_y)].append('S')
    maze[(goal_x, goal_y)].append('G')

    carve_path(start_x, start_y)

    return maze, (start_x, start_y), (goal_x, goal_y)



def print_maze(maze, width, height):
    for y in range(height):
        for x in range(width):
            print(' '.join(maze[(x, y)]), end=' ')
        print()


# def clearPreviousSolve(self):
#     self.results = dict()
#     self.untried = dict()
#     self.unbacktracked = dict()






        # Function to handle maze solving with timeout
def isMazeSolvable(timeLimit,maze):
    def solve_maze():
        maze.solve()
    thread = threading.Thread(target=solve_maze)
    thread.start()
    time.sleep(timeLimit)

    if thread.is_alive():
   
        # Maze solving is taking too long, generate a new maze
        print("Maze solving is taking too long. Generating a new maze...")
        




    
        return -1
      
    return 0
    

    
def evaluation(maze_size, simulations): 
    random_number = random.random()
    random_integer = random.randint(1, 1000)
    maze_alg_evaluation.doc_name = str(random_integer) + "_" + "mazesize_" + str(maze_size) + "_simulations_" + str(simulations) + ".txt"
    maze_alg_evaluation.file = open(maze_alg_evaluation.doc_name, 'w')

    environment, goal, loc = None, None, None
    generated = -1
    nonDirected_Dfs_num_actions = 0
    nonDirected_DfsSims = []
    directed_DfsSims = []
    nonDirected_Dfs_times = 0
    directed_Dfs_times = 0
    directed_Dfs_num_actions = 0
    numSim = 0
    while numSim < simulations:

        generated = -1
        while generated == -1:
       
            environment, goal, loc = generate_maze(maze_size, maze_size)
            evaluation_maze = maze(environment, goal, loc, maze_size, maze_size)
            generated = isMazeSolvable(3, evaluation_maze)

        # environment, goal, loc = generate_maze(maze_size, maze_size)
        evaluation_maze = maze(environment, goal, loc, maze_size, maze_size)
        nonDirected_Dfs = evaluation_maze.solve()
        nonDirected_Dfs_time = nonDirected_Dfs[1]
        nonDirected_Dfs = nonDirected_Dfs[0]
        evaluation_maze = maze(environment, goal, loc, maze_size, maze_size)
        directed_Dfs = evaluation_maze.solveDir()
        directed_Dfs_time = directed_Dfs[1]
        directed_Dfs = directed_Dfs[0]

        nonDirected_Dfs_num_actions = nonDirected_Dfs_num_actions + len(nonDirected_Dfs)
        directed_Dfs_num_actions =  directed_Dfs_num_actions + len(directed_Dfs)
        directed_Dfs_times = directed_Dfs_times + directed_Dfs_time
        nonDirected_Dfs_times = nonDirected_Dfs_times + nonDirected_Dfs_time
        nonDirected_DfsSims.append(nonDirected_Dfs)
        directed_DfsSims.append(directed_Dfs)

        print("Simulation " + str(numSim) + "\n" +  "Non-directed DFS Number of Actions: " + str(len(nonDirected_Dfs)) + "\n" + "Directed DFS Number of Actions: " + str(len(directed_Dfs)) + "\n" + "Non-directed DFS Solve Time: " + str(nonDirected_Dfs_time) + "\n" + "Directed DFS Solve Time: " + str(directed_Dfs_time) +"\n")
        maze_alg_evaluation.file.write("Simulation " + str(numSim) + "\n" +  "Non-directed DFS Number of Actions: " + str(len(nonDirected_Dfs)) + "\n" + "Directed DFS Number of Actions: " + str(len(directed_Dfs)) + "\n" + "Non-directed DFS Solve Time: " + str(nonDirected_Dfs_time) + "\n" + "Directed DFS Solve Time: " + str(directed_Dfs_time) +"\n")
        maze_alg_evaluation.file.write("-------------------------------------------\n")
        numSim = numSim + 1

    results = (
        nonDirected_DfsSims,
        directed_DfsSims,
        nonDirected_Dfs_num_actions//simulations,
        directed_Dfs_num_actions//simulations,
        directed_Dfs_times//simulations,
        nonDirected_Dfs_times//simulations,
        "Ran for " +  str(simulations) + " simulations\n" +  "Avg Non-directed DFS Number of Actions: " + str(nonDirected_Dfs_num_actions//simulations) + "\n" +  "Avg Directed DFS Number of Actions: " + str(directed_Dfs_num_actions//simulations) + "\n" +  "Avg Non-directed DFS Solve Time: " + str(nonDirected_Dfs_times/simulations) + "\n" + "Avg Directed DFS Solve Time: " + str(directed_Dfs_times/simulations)
       
    )

    return results


def main():
    loc = (0,0)
    environment = {
        (0,0) : [],
        (0,1) : ['U', 'R'],
        (0,2) : ['D'],
        (1,0) : [],
        (1,1) : ['L', 'R'],
        (1,2) : ['R'],
        (2,0) : [],
        (2,1) : ['L'],
        (2,2) : ['L']
    }
    goal = (2,2)

    # example_maze = maze(environment, goal, loc)
    # print("Starting: \n", "Loc: ", example_maze.loc, "Goal: ", example_maze.goal)
    # example_maze.solve()
    # print("Loc: ", example_maze.loc, "Goal: ", example_maze.goal)

    # environment, goal, loc = generate_maze(10, 10)
    # # print(environment, "\n", goal2, "\n", loc2)
    # maze2 = maze(environment2, goal2, loc2, 9, 9)
    # maze2.solve()
    results = evaluation(25, 3)
    print(results[6])

    maze_alg_evaluation.file.write(results[6])
    maze_alg_evaluation.file.close()
    os._exit(1) #Exits forceably if threads are still running

if __name__ == '__main__':
    main()

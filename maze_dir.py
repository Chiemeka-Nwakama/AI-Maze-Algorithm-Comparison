import contextlib
import random


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
        

    def possible_actions(self, loc):
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
    
    def solve(self):
        a = None
        s_prev = None
        s_curr = self.loc
        actions_taken = []

        while True:
            a = self.online_dfs_Agent(s_curr, s_prev, a)
            if a == None: break
            s_prev = s_curr
            s_curr = self.result(a)
            actions_taken.append(a)
            # print("Loc: ", self.loc, "Action: ", a) # Used to debug
        print("actions_taken ==", actions_taken)
        return actions_taken

    def online_dfs_Agent(self, s_curr, s_prev, a):
        if self.isGoal() == True: return None
        if s_curr not in self.untried:
            self.untried.update({s_curr: self.possible_actions(s_curr)})
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

import random

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

    environment2, goal2, loc2 = generate_maze(10, 10)
    print(environment2, "\n", goal2, "\n", loc2)
    maze2 = maze(environment2, goal2, loc2, 9, 9)
    maze2.solve()


if __name__ == '__main__':
    main()

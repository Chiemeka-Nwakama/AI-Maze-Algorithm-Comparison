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
    def __init__(self, environment, goal, loc = (0,0)):
        self.environment = environment
        self.loc = loc
        self.goal = goal
        self.results = dict()
        self.untried = dict()
        self.unbacktracked = dict()

    def possible_actions(self, loc):
        walls = self.environment[loc]
        actions = ['U', 'D', 'R', 'L'] # TODO: randomize this line
        if loc[1] == 0:
            with contextlib.suppress(ValueError):
                actions.remove('D')
        if loc[0] == 0:
            with contextlib.suppress(ValueError):
                actions.remove('L')
        if loc[1] == 2:
            with contextlib.suppress(ValueError):
                actions.remove('U')
        if loc[0] == 2:
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
        
    
    def isGoal(self):
        return self.loc == self.goal
    
    def solve(self):
        a = None
        s_prev = None
        s_curr = self.loc
        actions_taken = []

        while True:
            a = self.online_dfs_Agent(s_curr, s_prev, a)
            if a == None: break
            # s_curr = self.result(a, s_curr)
            s_curr = self.result(a)
            actions_taken.append(a)
            # print("loc == ", self.loc, "\n action == ", a) # used for debugging
        # print(self.loc, " == ", self.goal) # used for debugging 
        print("actions_taken ==", actions_taken)
        # print("trimed == ", self.trim_actions(actions_taken))    # self.trim_actions not working 
        # return self.trim_actions(actions_taken)  # Want to return this once self.trim_actions works
        return actions_taken

    def online_dfs_Agent(self, s_curr, s_prev, a):
        if self.isGoal() == True: return None
        if s_curr not in self.untried:
            self.untried.update({s_curr: self.possible_actions(s_curr)})
        if s_prev != None:
            self.results.update({s_curr: (s_prev, a)})
            self.unbacktracked.update({s_curr: s_prev})
        if not self.untried[s_curr]: # returns True if list is empty
            if not self.unbacktracked[s_curr]: return None
            else: 
                a = self.unbacktracked[s_curr].pop(0)
        else:
            a = self.untried[s_curr].pop(0)
        s_prev = s_curr
        # print(self.unbacktracked)
        return a
    
    



def generate_maze(x):
    '''
    Generate a random maze of size x by x that is solvable from (0, 0) to (x-1, x-1).

    x: An integer representing the size of the maze.

    Returns: A tuple containing a dictionary with integer pairs as the key and information about walls as the value and a tuple representing the goal location.
    '''
    # Initialize the maze
    maze = {}
    for i in range(x):
        for j in range(x):
            maze[(i, j)] = []

    # Generate the maze
    visited = set()
    stack = [(0, 0)]
    while stack:
        current = stack.pop()
        visited.add(current)
        neighbors = [(current[0] - 1, current[1]), (current[0] + 1, current[1]), (current[0], current[1] - 1), (current[0], current[1] + 1)]
        random.shuffle(neighbors)
        for neighbor in neighbors:
            if neighbor in visited or neighbor[0] < 0 or neighbor[0] >= x or neighbor[1] < 0 or neighbor[1] >= x:
                continue
            if neighbor[0] == current[0] - 1:
                maze[current].append('U')
                maze[neighbor].append('D')
            if neighbor[0] == current[0] + 1:
                maze[current].append('D')
                maze[neighbor].append('U')
            if neighbor[1] == current[1] - 1:
                maze[current].append('L')
                maze[neighbor].append('R')
            if neighbor[1] == current[1] + 1:
                maze[current].append('R')
                maze[neighbor].append('L')
            stack.append(neighbor)

    # Set the goal location
    goal = (x - 1, x - 1)

    # Return the maze and the goal location
    return maze, goal




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

    example_maze = maze(environment, goal, loc)
    environment2, goal2 = generate_maze(25)
    print(environment2)
    print(goal2)

    example_maze2 = maze(environment2, goal2, loc)

    # Checking possible_actions works correctly 
    # i = 0
    # for x in range(0,3):
    #     print("X change: ", x)
    #     for y in range(0, 3):
    #         print(i, ".)  ", "(", x, ", ", y, ")")
    #         actions = example_maze.possible_actions((x,y))
    #         print(actions)
    #         i += 1

    # Checking result() works correctly 
    # i = 0
    # for x in range(0,3):
    #     print("X change: ", x)
    #     for y in range(0, 3):
    #         print(i, ".)  ", "(", x, ", ", y, ")")
    #         actions = example_maze.possible_actions((x,y))
    #         print(actions)
    #         for a in actions:
    #             example_maze.loc = (x,y)
    #             print(a, "  =====  ", example_maze.result(a))
    #         i += 1

    example_maze2.solve()


if __name__ == '__main__':
    main()

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
            print("Loc: ", self.loc, "Action: ", a)
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

def generate_maze(x):
    n = x
    m = x
    maze = [[0 for j in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m):
            if i == 0 and j == 0:
                maze[i][j] = ['R', 'D']
            elif i == 0 and j == m - 1:
                maze[i][j] = ['L', 'D']
            elif i == n - 1 and j == 0:
                maze[i][j] = ['R', 'U']
            elif i == n - 1 and j == m - 1:
                maze[i][j] = ['L', 'U']
            elif i == 0:
                maze[i][j] = ['L', 'R', 'D']
            elif i == n - 1:
                maze[i][j] = ['L', 'R', 'U']
            elif j == 0:
                maze[i][j] = ['R', 'U', 'D']
            elif j == m - 1:
                maze[i][j] = ['L', 'U', 'D']
            else:
                maze[i][j] = ['L', 'R', 'U', 'D']

    visited = set()
    stack = [(0, 0)]
    while stack:
        (i, j) = stack.pop()
        visited.add((i, j))

        neighbors = []
        if i > 0 and (i - 1, j) not in visited:
            neighbors.append((i - 1, j))
        if i < n - 1 and (i + 1, j) not in visited:
            neighbors.append((i + 1, j))
        if j > 0 and (i, j - 1) not in visited:
            neighbors.append((i, j - 1))
        if j < m - 1 and (i, j + 1) not in visited:
            neighbors.append((i, j + 1))

        if neighbors:
            (ni, nj) = random.choice(neighbors)
            if ni < i:
                maze[i][j].remove('U')
                maze[ni][nj].remove('D')
            elif ni > i:
                maze[i][j].remove('D')
                maze[ni][nj].remove('U')
            elif nj < j:
                maze[i][j].remove('L')
                maze[ni][nj].remove('R')
            elif nj > j:
                maze[i][j].remove('R')
                maze[ni][nj].remove('L')

            stack.append((i, j))
            stack.append((ni, nj))

    goal = (n - 1, m - 1)
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
    # print("Starting: \n", "Loc: ", example_maze.loc, "Goal: ", example_maze.goal)
    example_maze.solve()
    # print("Loc: ", example_maze.loc, "Goal: ", example_maze.goal)

    environment2, goal2 = generate_maze(10)
    print(environment2)
    maze2 = maze(environment2, goal2, loc)
    # maze2.solve()


if __name__ == '__main__':
    main()

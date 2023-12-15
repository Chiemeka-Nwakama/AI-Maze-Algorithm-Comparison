# def outer_func():
#     outer_func.s_curr = (0,0)
#     def inner_func():
#         outer_func.s_curr = (outer_func.s_curr[0] + 1, outer_func.s_curr[1])    
#     inner_func()
#     print(outer_func.s_curr)

# outer_func()


# def make_list(loc, goal):
#     X_dir = goal[0] - loc[0]
#     Y_dir = goal[1] - loc[1]
#     full = ['U', 'D', 'R', 'L']
#     ret_list = []
    
#     if (abs(X_dir) >= abs(Y_dir)):
#         if X_dir > 0:
#             ret_list.append('U')
#         else:
#             ret_list.append('D')
#         if Y_dir > 0:
#             ret_list.append('R')
#         else:
#             ret_list.append('L')
#         # print(ret_list) # Used to debug
#         return ret_list + list(set(full) - set(ret_list))

#     if (abs(X_dir) < abs(Y_dir)):
#         if X_dir > 0:
#             ret_list.append('U')
#         else:
#             ret_list.append('D')
#         if Y_dir > 0:
#             ret_list.append('R')
#         else:
#             ret_list.append('L')
#         # print(ret_list) # Used to debug
#         return ret_list + list(set(full) - set(ret_list))

# print(make_list((0,0), (2,2)))

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
    carve_path(start_x, start_y)

    return maze

def print_maze(maze, width, height):
    for y in range(height):
        for x in range(width):
            print(' '.join(maze[(x, y)]), end=' ')
        print()

# Example usage
width, height = 11, 11  # Adjust as needed
maze_dict = generate_maze(width, height)
print_maze(maze_dict, width, height)
print(maze_dict)









################## BACKUP ###################

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
        
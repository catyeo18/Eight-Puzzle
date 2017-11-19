import numpy as np
from typing import List, Tuple
from collections import deque


def get_puzzle(shape: Tuple[int, int]=(3, 3)) -> Tuple:
    """
    0 denotes the blank space.
    :param shape: the shape of the puzzle. If an int is given, it will be a square of that size. If two ints are given,
                  it will be a rectangle of that shape.
    :returns:
    """

    size = np.prod(shape)
    num_inversions = 1  # so that we go into the while loop
    while num_inversions % 2 != 0:
        puzzle = np.random.permutation(np.arange(size))

        num_inversions = 0
        for i in range(len(puzzle)):
            if puzzle[i] == 0:
                continue  # ignore blank space
            for j in range(i):  # all spaces before this one
                if puzzle[j] > puzzle[i]:
                    num_inversions += 1

    return tuple(puzzle)


def get_goal_state(shape: Tuple[int, int]=(3, 3)) -> Tuple:
    """
    0 denotes the blank space.
    :param shape: the shape of the puzzle. If an int is given, it will be a square of that size. If two ints are given,
                  it will be a rectangle of that shape.
    :returns:
    """
    return tuple(range(1, np.prod(shape))) + (0,)


class Puzzle(object):
    def __init__(self, shape: Tuple[int, int]):
        """
        1x1 is not supported
        :param shape: height, length
        """

        self.height = shape[0]
        self.length = shape[1]
        self.size = self.length * self.height

        # set up parameters needed for computing neighbors for a puzzle of this size

        left_swap = -1  # sliding left means the index goes down one
        right_swap = 1  # up one for a right slide
        top_swap = -self.length  # moving up is like moving backwards an entire length
        bottom_swap = self.length

        idx = {
            'top': tuple(range(self.length)),
            'left': tuple(range(0, self.size, self.length)),
            'right': tuple(range(self.length - 1, self.size, self.length)),
            'bottom': tuple(range(self.size - self.length, self.size))
        }

        valid_swaps = {
            'left': [right_swap, top_swap, bottom_swap],
            'right': [left_swap, top_swap, bottom_swap],
            'top': [left_swap, right_swap, bottom_swap],
            'bottom': [left_swap, right_swap, top_swap]
        }

        valid_swaps_top_left_corner = [right_swap, bottom_swap]
        valid_swaps_top_right_corner = [left_swap, bottom_swap]
        valid_swaps_bottom_left_corner = [right_swap, top_swap]
        valid_swaps_bottom_right_corner = [left_swap, top_swap]

        all_swaps = [left_swap, right_swap, top_swap, bottom_swap]

        # {zero_idx: [valid_swaps]}
        self.valid_swaps = {i: valid_swaps[direction] for direction in idx for i in idx[direction]}

        # add in all of the points not on an edge
        for i in range(self.size):
            if i not in self.valid_swaps:
                self.valid_swaps[i] = all_swaps

        # fix the corners
        self.valid_swaps[0] = valid_swaps_top_left_corner
        self.valid_swaps[self.length - 1] = valid_swaps_top_right_corner
        self.valid_swaps[self.size - self.length] = valid_swaps_bottom_left_corner
        self.valid_swaps[self.size - 1] = valid_swaps_bottom_right_corner

    def swap(self, state: Tuple[int], i: int, j: int) -> Tuple[int]:
        """
        Swaps two elements in the given state tuple.
        :param state: a tuple with the current state of a puzzle
        :type state: tuple
        :param i: index of one element to swap
        :param j: index of other element to swap; j != i
        :return: a tuple which is a copy of state except the elements at i, j are swapped
        """

        first, second = sorted([i, j])
        swapped = (*state[:first], state[second], *state[first + 1: second], state[first], *state[second + 1:])
        #         swapped = state[:first] + (state[second],) + state[first+1:second] + (state[first],) + state[second+1:]
        return swapped

    def neighbors(self, state):
        """
        Returns a list of all the states reachable from the given state with one slide
        :type state: tuple
        :param state: the state from which to
        :return: a list of states that are reachable with one slide
        """

        blank_idx = state.index(0)  # where the blank spot is; slides have to move a piece to here
        return [self.swap(state, blank_idx, blank_idx + swap) for swap in self.valid_swaps[blank_idx]]


def print_path(path: List[Tuple[int]], shape: Tuple[int, int]):
    print([np.array(path[i]).reshape(shape).tolist() for i in range(len(path))])


#### YOUR CODE HERE #####

puzzle_shape = (3, 3)
start = get_puzzle(puzzle_shape) # randomly makes a puzzle for you
goal = get_goal_state(puzzle_shape) # get to this state to win!

print("Starting puzzle state:", start) # this is stored as 1D, but it represents a 3x3 puzzle
print("Goal state:", goal)

# this defines the function to get neighbors from a given puzzle node
puzzle_helper = Puzzle(puzzle_shape)

print("Neighbors of starting state:", puzzle_helper.neighbors(start))


### WRITE YOUR FUNCTION HERE
# it should return a path: a list of nodes which begins with start and ends with goal

expanded = set()
parents = {}
parents[start] = None
fringe = deque()

fringe.append((start, None))

while fringe:
  next_node, parent = fringe.popleft()
  parents[next_node] = parent
  if next_node == goal:
    print('Found goal!')
    break
  
  if next_node in expanded:
    continue
  
  neighbors = puzzle_helper.neighbors(next_node)
  for i in neighbors:
    if i not in expanded:
      fringe.append((i, next_node))
      
  expanded.add(next_node)
    

# find path

path = []
current_node = goal
while True:
  if current_node == None:
    break
  path.append(current_node)
  current_node = parents[current_node]

path.reverse()

print("Path:")
print_path(path, puzzle_shape)

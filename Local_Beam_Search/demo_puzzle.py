import itertools
import requests
import io
import time
from PIL import Image as PILImage
from problem import Eight_puzzle
from problem_solver import Local_beam_search_solver

def evaluate_func(state):
    h = 0
    
    for i, row in enumerate(state):
        for j, tile_state in enumerate(row):
            if tile_state[0] != i or\
            tile_state[1] != j:
                h += 1
    return h

def flat_state(state):
    return [y for x in state for y in x]

def pack_state(state):
    return tuple((state[i], state[i + 1], state[i + 2]) for i in [0, 3, 6])

def iter_states(state):
    flatted_state = flat_state(state)
    for pos_state in itertools.permutations(flatted_state):
        yield pack_state(pos_state)
        
def iter_neighbors(state):
    for i, row in enumerate(state):
        for j, tile_state in enumerate(row):
            if tile_state[2]:
                x, y = j, i
                break
    if x > 0:
        t = list([list(x) for x in state])
        t[y][x - 1], t[y][x] = t[y][x], t[y][x - 1]
        yield tuple([tuple(x) for x in t])

    if x < 2:
        t = list([list(x) for x in state])
        t[y][x + 1], t[y][x] = t[y][x], t[y][x + 1]
        yield tuple([tuple(x) for x in t])

    if y > 0:
        t = list([list(x) for x in state])
        t[y - 1][x], t[y][x] = t[y][x], t[y - 1][x]
        yield tuple([tuple(x) for x in t])

    if y < 2:
        t = list([list(x) for x in state])
        t[y + 1][x], t[y][x] = t[y][x], t[y + 1][x]
        yield tuple([tuple(x) for x in t])
        
img_bytes = requests.get('https://cloud.vinhthanh.net/s/zYcrxnYrd9FDTAL/download/twice.jpg', timeout = 8).content
img = PILImage.open(io.BytesIO(img_bytes))
img = img.resize((900, 900))
puzzle = Eight_puzzle(img, (2, 2))
puzzle.shuffle(30)
print(puzzle.show())
solver = Local_beam_search_solver()
solver.train(puzzle, evaluate_func, iter_states, iter_neighbors)
start = time.time()
solution = solver.solve(300, 5000, 5000)
end = time.time()
for row in solution:
    print(row)
print(end - start)
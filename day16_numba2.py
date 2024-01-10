'''Aoc Day16 Part1
walk the light bean through the map and count up active tiles'''
import time
from numba import njit, prange
import numpy as np

filename = 'input16.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

m = []
for l in ls:
    m.append([x for x in l])

directions = {'N':(-1,0), 'E':(0,1), 'S':(1,0), 'W':(0,-1)}
get_dir = {directions[key]:key for key in directions.keys()}

def solve(m, sy, sx, sd):
    '''Run the solve for a given starting tile and direction. Return the
    total number of energized tiles'''
    m_history = []
    for r in m:
        m_history.append([[] for x in r])

    # currently active light beams
    beams = [[sy, sx, sd]]
    
    while len(beams) > 0:
        cur_y, cur_x, cur_d = beams.pop()
        new_y = cur_y + cur_d[0]
        new_x = cur_x + cur_d[1]
        # test for going off map
        if new_y < 0 or new_x < 0 or new_y >= len(m) or new_x >= len(m[0]):
            continue
        new_tile = m[new_y][new_x]
        if new_tile == '.':
            if cur_d not in m_history[new_y][new_x]:
                m_history[new_y][new_x].append(cur_d)
                beams.append([new_y, new_x, cur_d])
                continue
            else:
                continue
        if new_tile == '/':
            if get_dir[cur_d] == 'N':
                new_d = directions['E']
            elif get_dir[cur_d] == 'E':
                new_d = directions['N']
            elif get_dir[cur_d] == 'S':
                new_d = directions['W']
            elif get_dir[cur_d] == 'W':
                new_d = directions['S']
            else:
                print("Error: setting new direction /")
            if new_d not in m_history[new_y][new_x]:
                m_history[new_y][new_x].append(new_d)
                beams.append([new_y, new_x, new_d])
                continue
            else:
                continue
        if new_tile == '\\':
            if get_dir[cur_d] == 'N':
                new_d = directions['W']
            elif get_dir[cur_d] == 'E':
                new_d = directions['S']
            elif get_dir[cur_d] == 'S':
                new_d = directions['E']
            elif get_dir[cur_d] == 'W':
                new_d = directions['N']
            else:
                print("Error: setting new direction /")
            if new_d not in m_history[new_y][new_x]:
                m_history[new_y][new_x].append(new_d)
                beams.append([new_y, new_x, new_d])
                continue
            else:
                continue
        if new_tile == '-':
            cur_ds = get_dir[cur_d]
            if cur_ds == 'E' or cur_ds == 'W':
                if cur_d not in m_history[new_y][new_x]:
                    m_history[new_y][new_x].append(cur_d)
                    beams.append([new_y, new_x, cur_d])
                    continue
                else:
                    continue
            elif cur_ds == 'N' or cur_ds == 'S':
                # split in two
                new_d = directions['W']
                if new_d not in m_history[new_y][new_x]:
                    m_history[new_y][new_x].append(new_d)
                    beams.append([new_y, new_x, new_d])
                new_d = directions['E']
                if new_d not in m_history[new_y][new_x]:
                    m_history[new_y][new_x].append(new_d)
                    beams.append([new_y, new_x, new_d])
                continue
            else:
                print("Error: In new tile -")
        if new_tile == '|':
            cur_ds = get_dir[cur_d]
            if cur_ds == 'N' or cur_ds == 'S':
                if cur_d not in m_history[new_y][new_x]:
                    m_history[new_y][new_x].append(cur_d)
                    beams.append([new_y, new_x, cur_d])
                    continue
                else:
                    continue
            elif cur_ds == 'W' or cur_ds == 'E':
                # split in two
                new_d = directions['N']
                if new_d not in m_history[new_y][new_x]:
                    m_history[new_y][new_x].append(new_d)
                    beams.append([new_y, new_x, new_d])
                new_d = directions['S']
                if new_d not in m_history[new_y][new_x]:
                    m_history[new_y][new_x].append(new_d)
                    beams.append([new_y, new_x, new_d])
                continue
            else:
                print("Error: In new tile |")
        else:
            print("Error: Ran out of new tile types")

    # we should now be able to count up non-zero histories
    
    total = 0
    for r in m_history:
        for c in r:
            if len(c) > 0:
                total += 1
    return(total)

T0 = time.perf_counter()
ans = solve(m, 0, -1, directions['E'])
T1 = time.perf_counter()

print("Part 1 total energized tiles is", ans, "and took", T1 - T0, "seconds")

'''Part 2 - find the maximum total starting along every edge position
pointing inward'''
max_total = 0
# pointing south along the top
@njit(forceobj=True, parallel=True)
def sideSolveX(m, yi, d, s):
    max_totals = np.zeros(s)
    for x in prange(s):
        max_totals[x] = solve(m, yi, x, d)
    cur_max = max_totals.max()
    return(cur_max)

T0 = time.perf_counter()
s = len(m[0])
d = directions['S']
cur_max = sideSolveX(m, -1, d, s)
if cur_max > max_total:
    max_total = cur_max
# pointing north along the bottom
for x in range(len(m[0])):
    cur_total = solve(m, len(m), x, directions['N'])
    if cur_total > max_total:
        max_total = cur_total
# pointing east along the west edge
for y in range(len(m)):
    cur_total = solve(m, y, -1, directions['E'])
    if cur_total > max_total:
        max_total = cur_total
# pointing west along the east edge
for y in range(len(m)):
    cur_total = solve(m, y, len(m[0]), directions['W'])
    if cur_total > max_total:
        max_total = cur_total
T1 = time.perf_counter()

print("Part 2 maximum energized tiles is", max_total, "in", T1 - T0,
      "seconds")

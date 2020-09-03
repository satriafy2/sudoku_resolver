import re
import random
import json

def _check_grid(on_work, idx, val):
    y_axis = idx % 9
    i_axis = int(idx / 9)
    i_grid  = (i_axis - (i_axis % 3)) + round(((i_axis / 3) + 0.5))
    i_grid  = (i_grid - 1) if i_grid > 0 else 0

    start = int(i_grid / 3) * 27
    index = start

    for start in range(start + 9):
        if on_work[index] == val:
            return False

        if ( (start + 1) % 3 ) != 0:
            index += 1

        else:
            index += 9

    return True


def _check_x_y(puzzle, idx, val):
    # check x axis
    start   = int(idx / 9) * 9
    end     = start + 9

    while start < end:
        if puzzle[start] == val:
            return False

        start +=1

    # check y axis
    start   = idx % 9
    end     = start * 9

    while start < end:
        if puzzle[start] == val:
            return False

        start += 1

    return True


def _new_solve_puzzle(puzzle):
    on_work = puzzle[:]
    onward  = True
    i = 0

    while i < len(puzzle):
        # print(f"[{i}] Puzzle - {puzzle[i]} | Current work - {on_work[i]}")
        if puzzle[i] == 0:
            j = 0
            while j <= 9:
                random_val = random.randint(1, 9)
                # print(f"[{i}] Try - {random_val}")

                if _check_x_y(on_work, i, random_val) \
                and _check_grid(on_work, i, random_val) \
                and random_val != on_work[i]:
                    on_work[i]  = random_val
                    # print(f"[{i}] Replace - {random_val}")
                    onward      = True
                    break

                elif j == 9:
                    on_work[i] = 0
                    onward = False

                j+= 1

        if onward:
            i += 1
            # print(f'Keep going -> [{i}]')

        else:
            i -= 1
            # print(f'Backward  -> [{i}]')

    return on_work


print('Please insert the string puzzle')
sudoku_string = input()
sudoku_string = list(re.sub('[\s+]', '', sudoku_string))
sudoku_list   = list(map(int, sudoku_string))

grids  = _into_grid(sudoku_list)
x_list = _into_x(sudoku_list)
y_list = _into_y(sudoku_list)

solved = _new_solve_puzzle(sudoku_list)

print(solved)

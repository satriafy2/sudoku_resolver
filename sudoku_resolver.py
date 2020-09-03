import re
import random
import json


def _write_into_file(grids, x, y):
    converted = {
        'grids': grids,
        'x_axis': x,
        'y_axis': y
    }

    converted_json = json.dumps(converted)
    text_file = open("json_data.txt", "w")
    text_file.write(converted_json)
    text_file.close()


def _into_x(data):
    x_axis, temp  = [], []

    for i, v in enumerate(data):
        temp.append(v)

        if ((i + 1) % 9) == 0:
            x_axis.append(temp)
            temp = []

    return x_axis


def _into_y(data):
    y_axis, i = [], 0

    while i < 9:
        temp = []
        j, index = 0, i

        while j < 9:
            temp.append(data[index])
            index += 9
            j += 1

        y_axis.append(temp)
        i += 1

    return y_axis


def _into_grid(data):
    grid, tempg, temp = [], [], []

    x = 0
    while x < len(data):
        temp.append(data[x])

        if (x+1) % 3 == 0:
            tempg.append(temp)
            temp = []

        x+=1

    i = 0
    while i < len(tempg):
        new_list = tempg[i] + tempg[i+3] + tempg[i+6]
        grid.append(new_list)

        if (i+1) % 3 == 0:
            i+=7

        else:
            i+=1

    return grid


def _static_index(sudoku_puzzle):
    list_istatic = []
    for i in range(len(sudoku_puzzle)):
        if sudoku_puzzle[i] == 0:
            list_istatic.append(i)

    return list_istatic


def _replace_x(idx, x_list, value):
    i_replace = x_list[idx].index(0)
    x_list[idx][i_replace] = value

    return x_list


def _replace_y(idx, y_list, value):
    i_replace = y_list[idx].index(0)
    y_list[idx][i_replace] = value

    return y_list


def _replace_grid(idx, grids, value):
    i_replace = grids[idx].index(0)
    grids[idx][i_replace] = value

    return grids


def _store_possible_number(index, val):
    pass


def _generate_combination(combination_list, static_index):

    def _check_all_nine(c_list):
        all_nine = True

        for x in range(len(c_list)):
            if x not in static_index:
                if c_list[x] < 9 or c_list[x] > 9:
                    all_nine = False
                    break

        return all_nine


    last_idx = len(combination_list) - 1

    x = last_idx
    while x >= 0:
        if x not in static_index:
            combination_list[x] += 1

            if _check_all_nine(combination_list):
                y = 0

                while y < len(combination_list):
                    combination_list[y] = 1
                    y += 1

                combination_list.append(1)
                break

            elif combination_list[x] > 9:
                combination_list[x] = 1

            else:
                break

        x -= 1

    return combination_list


def _solve_puzzle(sudoku_list, grids, x_list, y_list, max_try, lock_cmb):
    x = 0

    while x < len(sudoku_list):
        sudoku_value = sudoku_list[x]
        print(x, len(lock_cmb))

        if sudoku_value == 0:
            rand_limit, counter = max_try, 0
            rand_stop = False

            i_yaxis = x % 9
            i_xaxis = int(x / 9)
            i_grid  = (i_xaxis - (i_xaxis % 3)) + round(((i_yaxis / 3) + 0.5))
            i_grid  = (i_grid - 1) if i_grid > 0 else 0

            while not rand_stop and counter < rand_limit:
                counter += 1

                if x < len(lock_cmb):
                    rand_value = lock_cmb[x]

                else:
                    rand_value = random.randint(1, 9)

                if rand_value not in x_list[i_xaxis] \
                    and rand_value not in y_list[i_yaxis] \
                    and rand_value not in grids[i_grid]:

                    grids  = _replace_grid(i_grid, grids, rand_value)
                    x_list = _replace_x(i_xaxis, x_list, rand_value)
                    y_list = _replace_y(i_yaxis, y_list, rand_value)

                    rand_stop = True

                if counter == max_try:
                    rand_stop = True
                    return {
                        'result': False,
                        'lock_cmb': lock_cmb
                    }

        x += 1

    return {'result': True}


def _check_grid(on_work, idx, val):
    y_axis = idx % 9
    i_axis = int(idx / 9)
    i_grid  = (i_axis - (i_axis % 3)) + round(((i_axis / 3) + 0.5))
    i_grid  = (i_grid - 1) if i_grid > 0 else 0

    start = int(i_grid / 3) * 27
    index = start

    for start in range(start + 9)
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

    # check y axis
    start   = idx % 9
    end     = start * 9

    while start < end:
        if puzzle[start] == val:
            return False

    return True


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

#     while i < len(puzzle):
    while i < 9:
        print(f"[{i}] Puzzle - {puzzle[i]} | Current work - {on_work[i]}")
        if puzzle[i] == 0:
            j = 0
            while j <= 9:
                random_val = random.randint(1, 9)
                print(f"[{i}] Try - {random_val}")

                if _check_x_y(on_work, i, random_val) \
                and _check_grid(on_work, i, random_val) \
                and random_val != on_work[i]:
                    on_work[i]  = random_val
                    print(f"[{i}] Replace - {random_val}")
                    onward      = True
                    break

                elif j == 9:
                    on_work[i] = 0
                    onward = False

                j+= 1

        if onward:
            i += 1
            print(f'Keep going -> [{i}]')

        else:
            print(f'Backward  -> [{i}]')
            i -= 1

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

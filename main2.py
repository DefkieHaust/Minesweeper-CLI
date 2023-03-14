import random, time, os, sys

def gen_boxes(row, column):
    lst = []
    for i in range(1,row+1):
        for j in range(1,column+1):
            lst.append((i, j))
    return lst

def gen_mines(num, boxes, pos):
    forbidden = []
    up = pos[0] - 1
    left = pos[1] - 1
    for i in range(3):
        for j in range(3):
            key = (up+i, left+j)
            forbidden.append(key)
    s = set()
    while len(s) < num:
        n = random.choice(boxes)
        if n not in forbidden:
            s.add(n)
    return s

def show_mines():
    for mine in mines:
        if boxes.get(mine) != flagged:
            boxes.update({mine:showing})
        else:
            boxes.update({mine:flagged_showing})

def game_state():
    os.system("clear")
    if debug_mode:
        print("\033[1;33m(DEBUG MODE!)")
    print(f"\033[1;37m(Time: {round(time.time()-start)}sec, Flags left: {flags})")
    print("\n    ", end="")
    for i in range(1, box_columns+1):
        print(f"\033[1;37m{i:<3}", end="")
    print()
    lst = list(boxes.values())
    for i in range(box_rows):
        print(f"\033[1;37m{i+1:<3}", end="")
        for j in range(box_columns):
            index = j+(i*box_columns)
            print(f"{lst[index]}", end="")
        print()
    print()

def clear_lines(times):
    for i in range(times):
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')

def get_method():
    method = None
    print(f"\033[1;37m(Row: None, Column: None, Method: {method})")
    while method not in ["flag", "open"]:
        method = input("\033[1;0mSelect method (flag) or (open): \033[1;37m")
        if method == "quit":
            clear_lines(2)
            exit(quit_msg)
        clear_lines(1)
    clear_lines(1)
    return method

def get_pos(method):
    pos = {"row":None, "column":None}
    for key, value in pos.items():
        while value not in ([str(i) for i in range(1, box_rows+1)] if key == "row" else [str(i) for i in range(1, box_columns+1)]):
            print(f"\033[1;37m(Row: {pos_buffer.get('row')}, Column: {pos_buffer.get('column')}, Method: {method})")
            value = input(f"\033[1;0mWhich {key} do you {method}?: \033[1;37m")
            if value == "quit":
                clear_lines(2)
                exit(quit_msg)
            elif value in ["flag", "open"]:
                global _method
                method = _method = value
                clear_lines(2)
                return get_pos(method)
            elif value == "back":
                clear_lines(2)
                return get_pos(method)
            clear_lines(2)
        pos_buffer.update({key:int(value)})
        pos.update({key:int(value)})
    return ((pos.get('row'), pos.get('column')), method)

def attempt(method):
    box_num, method = get_pos(method)
    if method == "flag":
        flag_pos(box_num)
    elif boxes.get(box_num) == closed:
        open_pos(box_num)

def flag_pos(box_num):
    global flags
    if boxes.get(box_num) == closed and flags > 0:
        boxes.update({box_num:flagged})
        flags -= 1
    elif boxes.get(box_num) == flagged:
        boxes.update({box_num:closed})
        flags += 1

def open_pos(box_num):
    global first_run
    if first_run:
        global mines
        first_run = False
        mines = gen_mines(mines_sum, positions, box_num)
        if debug_mode: show_mines()
    if box_num in mines:
        show_mines()
        game_state()
        exit(lost_msg)
    est = []
    up = box_num[0] - 1
    left = box_num[1] - 1
    for i in range(3):
        for j in range(3):
            key = (up+i, left+j)
            if key in mines:
                est.append(key)
    if len(est) > 0:
        est = opened.replace(" ", str(len(est)))
        boxes.update({box_num:est})
    else:
        boxes.update({box_num:opened})
        for i in range(3):
            for j in range(3):
                key = (up+i, left+j)
                if key != box_num and boxes.get(key) == closed:
                    open_pos(key)
    global opens
    opens += 1

def runtime():
    while True:
        if first_run:
            game_state()
            attempt(_method)
            continue
        if len(positions) - len(mines) == opens:
            show_mines()
            game_state()
            exit(win_msg)
        game_state()
        attempt(_method)

if __name__ == "__main__":

### Game Layout Settings ###
    box_rows = 15
    box_columns = 15
    flags = round(box_rows*box_columns/5)

### Game Graphical Settings ###
    closed = "\033[1;32m[#]"
    flagged = "\033[1;34m[X]"
    opened = "\033[1;33m[ ]"
    showing = "\033[1;31m[B]"
    flagged_showing = "\033[1;34m[B]"

### Game Messages Settings ###
    win_msg = "\033[1;34mYou won!"
    lost_msg = "\033[1;31mYou lost!"
    quit_msg = "\033[1;37mYou quit the game."

### Game Generation Settings ###
    debug_mode = False
    opens = 0
    mines_sum = flags
    positions = gen_boxes(box_rows, box_columns)
    boxes = {key:closed for key in positions}
    mines = None
    pos_buffer = {"row":None, "column":None}
    first_run = True

### Game Startup ###
    start = time.time()
    game_state()
    _method = get_method()
    runtime()

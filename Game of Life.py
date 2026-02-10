#SETUP
import os
import time
import random

#COLORS
LIGHT_GREEN = "\033[1;32m"
GREEN = "\033[0;32m"
DARK_GRAY = "\x1b[0;38;2;46;90;90m"
FAINT_GREEN = "\x1b[0;38;2;96;255;96m"
ORANGE = "\x1b[0;38;2;243;184;3;49m"
RESET = "\033[0m"

#WHILE SETTING IS TRUE, SETS UP THE "RULES", WHILE SETUP IS TRUE, SETS UP THE GRID. WHILE RUN IS TRUE, RUNS THE SIMULATION
setting = True
setup = False
run = False
GRID_SIZE = 128
EMPTY_TILE = f"{DARK_GRAY}·{RESET}"
CELL_SPACING = " "
TIME_BETWEEN_GENERATIONS = 1
cursor_x, cursor_y = 0, 0
cells_created = 0
cells_deleted = 0
cells = 0
generation = 0
paused = False

def create_grid(size):
    global GRID_SIZE, grid, cell_grid
    GRID_SIZE = size

    grid = [[EMPTY_TILE for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    cell_grid = []
    Cell.members.clear()

    for y in range(GRID_SIZE):
        row = []
        for x in range(GRID_SIZE):
            row.append(Cell(x, y))
        cell_grid.append(row)

#CONSTRUCTS BLUEPRINT
GLIDER = [
    (0, 0),
    (1, 0),
    (2, 0),
    (2, 1),
    (1, 2),
]

LIGHTWEIGHT_SPACESHIP = [
    (1, 0),
    (2, 0),
    (3, 0),
    (4, 0),

    (0, 1),
    (4, 1),

    (4, 2),

    (0, 3),
    (3, 3),
]

GOSPER_GUN = [
    (0, 4), (0, 5), (1, 4), (1, 5),

    (10, 4), (10, 5), (10, 6),
    (11, 3), (11, 7),
    (12, 2), (12, 8),
    (13, 2), (13, 8),
    (14, 5),
    (15, 3), (15, 7),
    (16, 4), (16, 5), (16, 6),
    (17, 5),

    (20, 2), (20, 3), (20, 4),
    (21, 2), (21, 3), (21, 4),
    (22, 1), (22, 5),
    (24, 0), (24, 1), (24, 5), (24, 6),

    (34, 2), (34, 3),
    (35, 2), (35, 3)
]

#THIS FUNCTION TAKES ONE OF THE CONSTRUCT'S LIST'S NAME AND BUILDS IT
def place_construct(offsets):
    for dx, dy in offsets:
        x = cursor_x + dx
        y = cursor_y + dy
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            cell_grid[y][x].change_state()

class Cell() :
    global grid
    members = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = False
        self.next_alive = False
        self.age = 0
        self.color = LIGHT_GREEN
        Cell.members.append(self)

    def change_state(self):
        self.alive = not self.alive

#TRANSFER THE ALIVE STATE OF THE CELL TO ITS GRAPHIC GRID EQUIVALENT, AND GIVES IT A COLOR BASED ON ITS AGE
    def update(self):

        if self.age == 0 : self.color = FAINT_GREEN
        elif self.age  == 1 : self.color = LIGHT_GREEN
        elif self.age > 1 : self.color = GREEN
        else: self.color = LIGHT_GREEN

        if self.alive:
            grid[self.y][self.x] = f"{self.color}O{RESET}"
        else:
            grid[self.y][self.x] = EMPTY_TILE

    @classmethod
    def class_update(cls):
        for cell in cls.members:
            cell.update()

    @classmethod
    def class_check(cls):

#THOSE VARIABLES ARE USED ONLY TO KEEP TRACK OF THE DATA, SEE RUN FOR MORE INFO
        global cells_created, cells_deleted, cells, generation
        cells = 0

        for cell in cls.members:

            alive_neighbors = 0

#GENERATES A SQUARE AROUND THE CELL TO CHECK NEIGHBORS
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):

#SKIPS THE CELL WHOSE NEIGHBOR WE ARE CHECKING
                    if dx == 0 and dy == 0:
                        continue

                    nx = cell.x + dx
                    ny = cell.y + dy

#SKIPS NEIGHBORS OUTSIDE THE GRID (PREVENTS CRASHES)
                    if not (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE):
                        continue

                    alive_neighbors += cell_grid[ny][nx].alive

#APPLIES THE RULES, AND UPDATES DATA
            if cell.alive:
                cell.next_alive = alive_neighbors in (2, 3)
                if not cell.next_alive:
                    cells_deleted += 1
                    cell.age = 0
                else: cell.age += 1
            else:
                cell.next_alive = alive_neighbors == 3
                if cell.next_alive: cells_created += 1

#COUNTS CELLS FOR DATA
        for cell in cls.members:
            cell.alive = cell.next_alive
            if cell.alive : cells += 1

#CLEARS THE OLD GRID, COMPUTES AND PRINTS THE NEW GRAPHICS GRID.
def update():
    global cursor_x, cursor_y
    print("\033[2J\033[H", end="")

    Cell.class_update()
    if not run : grid[cursor_y][cursor_x] = "X"
    else : grid[cursor_y][cursor_x] = EMPTY_TILE

    for row in grid:
        print(CELL_SPACING.join(row))
    print()

while setting:
    print("xX----------------------------------------Xx")
    print(f"      {"\x1b[3;1;4;38;2;0;183;91;49m"}WELCOME TO THE GAME OF LIFE{RESET}")
    print("xX----------------------------------------Xx")
    print()
    print()
    print()
    print()
    print("What should be the size of the grid? (Recommended = 16, 32 or 64, but 118 is better (if your computer can take it))")
    print("Using values different than the recommended ones may hide part of the grid depending on your screen's resolution.")
    GRID_SIZE = int(input(">"))
    create_grid(GRID_SIZE)
    print()
    print()
    print("What should the time, in seconds, between generations be? (Recommended = 0.1 / 0.3)")
    TIME_BETWEEN_GENERATIONS = float(input(">"))
    print()
    print()
    print(f"You will now set up your simulation. {ORANGE}I recommend going fullscreen and zooming out until you see everything using ctrl + wheel once the grid loads.{RESET}")
    print("Press enter to continue...")
    input()
    os.system("cls" if os.name == "nt" else "clear")
    setting = False
    setup = True

    while setup :
        update()

        print("Move the cursor with ZQSD. If you are using a QWERTY keyboard, I recommend changing the code accordingly. Press enter after each key press. After going in a direction once, press enter to move in that same direction again")
        print("Enter 'p' to place or remove a cell at the cursor's position.")
        print("Enter 'c' to open the construct library.")
        print("Enter 'r' to randomly fill the grid.")
        print("Enter 'o' to reset the grid.")
        print("Enter 'l' to launch the simulation")
        move = input(">")

#MOVES THE CURSOR
        if move == "z":
            move_x = 0
            move_y = -1
        if move == "s":
            move_x = 0
            move_y = 1
        if move == "q":
            move_x = -1
            move_y = 0
        if move == "d":
            move_x = 1
            move_y = 0

#PLACES A CELL
        if move == "p":
            cell_grid[cursor_y][cursor_x].change_state()

#STARTS THE SIMULATION
        if move == "l":
            update()

            setup = False
            run = True

#PLACES CELLS RANDOMLY ON THE WHOLE GRID
        if move == "r":
            for cell in Cell.members:
                if random.choice([True, False]):
                    cell.change_state()

        if move == "o":
            for cell in Cell.members:
                cell.alive = False

            cells_created = 0
            cells_deleted = 0

#OPENS CONSTRUCT LIBRARY
        if move == "c":
            update()
            print("Here are some pre-made constructs. Enter your desired construct's number. Press enter to quit.")
            print("The construct will be placed at the cursor's position.")
            print("1. Glider")
            print("2. Lightweight Spaceship")
            print("3. Gosper Gun")
            construct = input(">")
            if construct == "1":
                place_construct(GLIDER)
            if construct == "2":
                place_construct(LIGHTWEIGHT_SPACESHIP)
            if construct == "3":
                place_construct(GOSPER_GUN)

        if move != "r" and move != "l" and move != "c" and move != "p":
            cursor_x += move_x
            cursor_y += move_y

        while run:
            if not paused :
                generation += 1

                Cell.class_check()

                density = cells * 100 / GRID_SIZE ** 2

                update()

                print("Press enter to pause, and 'q' to quit to setup.")
                print("Generation number " + str(generation))
                print("Number of cells alive : " + str(cells))
                print("Number of cells created : " + str(cells_created))
                print("Number of cells that died : " + str(cells_deleted))
                print("Density : " + str(round(density, 1)) + "%")
                time.sleep(TIME_BETWEEN_GENERATIONS)

            # NON-BLOCKING INPUT CHECK
            if os.name == "nt":
                import msvcrt

                if msvcrt.kbhit():
                    key = msvcrt.getwch()
                    if key == " ":
                        paused = not paused
                    elif key == "q":
                        run = False
                        setup = True

#SETUP
import os
import time
import random

#COLORS
LIGHT_GREEN = "\033[1;32m"
GREEN = "\033[0;32m"
DARK_GRAY = "\x1b[0;38;2;46;90;90m"
FAINT_GREEN = "\x1b[0;38;2;96;255;96m"
RESET = "\033[0m"

#WHILE SETTING IS TRUE, SETS UP THE "RULES", WHILE SETUP IS TRUE, SETS UP THE GRID. WHILE RUN IS TRUE, RUNS THE SIMULATION
setting = True
setup = False
run = False
GRID_SIZE = 64
EMPTY_TILE = f"{DARK_GRAY}·{RESET}"
CELL_SPACING = " "
TIME_BETWEEN_GENERATIONS = 1
cursor_x, cursor_y = 0, 0
cells_created = 0
cells_deleted = 0
cells = 0
generation = 0

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

    (0, 1),
    (3, 1),

    (3, 2),

    (0, 3),
    (2, 3),
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

#GRID IS THE GRAPHIC GRID, CELL_GRID IS THE COMPUTING GRID
grid = [[EMPTY_TILE for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
cell_grid = []

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
                if not cell.next_alive: cells_deleted += 1
                else: cell.age += 1
            else:
                cell.next_alive = alive_neighbors == 3
                if cell.next_alive: cells_created += 1

#COUNTS CELLS FOR DATA
        for cell in cls.members:
            cell.alive = cell.next_alive
            if cell.alive : cells += 1

#INITIALIZES THE GRID CELL, USED FOR COMPUTING.
for y in range(GRID_SIZE):
    row = []
    for x in range(GRID_SIZE):
        row.append(Cell(x, y))
    cell_grid.append(row)

#CLEARS THE OLD GRID, COMPUTES AND PRINTS THE NEW GRAPHICS GRID.
def update():
    global cursor_x, cursor_y
    os.system("cls" if os.name == "nt" else "clear")

    Cell.class_update()
    if not run : grid[cursor_y][cursor_x] = "X"
    else : grid[cursor_y][cursor_x] = EMPTY_TILE

    for row in grid:
        print(CELL_SPACING.join(row))
    print()

while setting:
    print(f"{"\x1b[3;1;4;38;2;0;183;91;49m"}WELCOME TO THE GAME OF LIFE{RESET}")
    print()
    GRID_SIZE = int(input("What should be the size of the grid? (Recommended = 64): "))
    TIME_BETWEEN_GENERATIONS = float(input("What should the time, in seconds, between generations be? (Recommended = 0.1 / 0.3): "))
    print("You will now set up your simulation. I recommand going fullscreen and zooming out using ctrl + wheel once the grid loads.")
    print("Press enter to continue...")
    input()
    setting = False
    setup = True

    while setup :
        update()

        print("Move the cursor with ZQSD. If you are using a QWERTY keyboard, I recommend changing the code accordingly. Press enter after each key press. To make this process more comfortable, put one hand over the enter key and the other over the movement keys.")
        print("Press 'p' to place or remove a cell at the cursor's position.")
        print("Press 'c' to open the construct library.")
        print("Press 'r' to randomly fill the grid.")
        print("Press 'l' to launch the simulation")
        move = input(">")
#MOVES THE CURSOR
        if move == "z":
            cursor_y -= 1
        if move == "s":
            cursor_y += 1
        if move == "q":
            cursor_x -= 1
        if move == "d":
            cursor_x += 1
#PLACES A CELL
        if move == "p":
            cell_grid[cursor_y][cursor_x].change_state()
#STARTS THE SIMULATION
        if move == "l":
            setup = False
            run = True
#PLACES CELLS RANDOMLY ON THE WHOLE GRID
        if move == "r":
            for cell in Cell.members:
                if random.choice([True, False]):
                    cell.change_state()
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

        while run:
            generation += 1
            Cell.class_check()
            density = cells * 100 / GRID_SIZE ** 2
            update()
            print()
            print("Generation number " + str(generation))
            print("Number of cells alive : " + str(cells))
            print("Number of cells created : " + str(cells_created))
            print("Number of cells that died : " + str(cells_deleted))
            print("Density : " + str(round(density, 1)) + "%")
            time.sleep(TIME_BETWEEN_GENERATIONS)

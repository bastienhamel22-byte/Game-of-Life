#SETUP

import os
import time

#WHILE SETTING IS TRUE, SETS UP THE "RULES", WHILE SETUP IS TRUE, SETS UP THE GRID. WHILE RUN IS TRUE, RUNS THE SIMULATION
setting = True
setup = False
run = False
GRID_SIZE = 64
EMPTY_TILE = "·"
CELL_SPACING = " "
TIME_BETWEEN_GENERATIONS = 1

#GRID IS THE GRAPHIC GRID, CELL_GRID IS THE COMPUTING GRID
grid = [[EMPTY_TILE for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
cell_grid = []



class Cell() :
    global grid
    members = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = False
        self.next_alive = False
        Cell.members.append(self)

    def change_state(self):
        self.next_alive = not self.alive

#TRANSFER THE ALIVE STATE OF THE CELL TO ITS GRAPHIC GRID EQUIVALENT
    def update(self):
        if self.alive:
            grid[self.y][self.x] = "O"
        else:
            grid[self.y][self.x] = EMPTY_TILE

    @classmethod
    def class_update(cls):
        for cell in cls.members:
            cell.update()

    @classmethod
    def class_check(cls):
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

#APPLIES THE RULES
            if cell.alive:
                cell.next_alive = alive_neighbors in (2, 3)
            else:
                cell.next_alive = alive_neighbors == 3

        for cell in cls.members:
            cell.alive = cell.next_alive

#INITIALIZES THE GRID CELL, USED FOR COMPUTING.
for y in range(GRID_SIZE):
    row = []
    for x in range(GRID_SIZE):
        row.append(Cell(x, y))
    cell_grid.append(row)

#CLEARS THE OLD GRID, COMPUTES AND PRINTS THE NEW GRAPHICS GRID.
def update():
    os.system("cls" if os.name == "nt" else "clear")

    Cell.class_update()

    for row in grid:
        print(CELL_SPACING.join(row))
    print()
while setting:
    GRID_SIZE = int(input("What should be the size of the grid? (Recommended = 64): "))
    TIME_BETWEEN_GENERATIONS = float(input("What should the time, in seconds, between generations be? (Recommended = 0.3 / 0.5): "))
    print("You will now set up your simulation. I recommand going fullscreen and zooming out using ctrl + wheel once the grid loads")
    print("Press enter to continue...")
    input()
    setting = False
    setup = True

    while setup :
        update()
        print("Enter a tile's coordinates to create a cell there.")
        print("Top left corner is 0, 0 and bottom right corner is " + str(GRID_SIZE - 1))
        swap_x = int(input("Enter the tile's x coordinate: "))
        swap_y = int(input("Enter the tile's y coordinate: "))
        cell_grid[swap_y][swap_x].change_state()
        cell_grid[swap_y][swap_x].alive = cell_grid[swap_y][swap_x].next_alive
        update()
        answer = input("To run the simulation, enter z. Enter anything else to continue setting up the simulation : ")
        if answer == "z" :
            setup = False
            run = True

        while run:
            Cell.class_check()
            update()
            time.sleep(TIME_BETWEEN_GENERATIONS)

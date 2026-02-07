#SETUP

import os
import time

#WHILE SETUP IS TRUE, SETS UP THE GRID. WHILE RUN IS TRUE, RUNS THE SIMULATION
setup = True
run = False
GRID_SIZE = 5
EMPTY_TILE = "·"
CELL_SPACING = " "

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
        Cell.members.append(self)

    def change_state(self):
        self.alive = not self.alive

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

#INITIALIZES THE GRID CELL, USED FOR COMPUTING.
for y in range(GRID_SIZE):
    row = []
    for x in range(GRID_SIZE):
        row.append(Cell(x, y))
    cell_grid.append(row)

#CLEARS THE OLD GRID, AND PRINTS THE NEW GRAPHICS GRID.
def update():
    os.system("cls" if os.name == "nt" else "clear")

    Cell.class_update()

    for row in grid:
        print(CELL_SPACING.join(row))
    print()

while setup :
    update()
    print("Enter a tile's coordinates to create a cell there.")
    swap_x = int(input("Enter the tile's x coordinate: "))
    swap_y = int(input("Enter the tile's y coordinate: "))
    cell_grid[swap_y][swap_x].change_state()
    update()
    answer = input("To run the simulation, enter z. Enter anything else to continue setting up the simulation : ")
    if answer == "z" :
        setup = False
        run = True

    while run:
        pass

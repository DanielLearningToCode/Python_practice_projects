import random

width = 100
height = 100


def create_grid():
    """creates two 2D lists 100*100"""
    global grid_model, next_grid_model
    grid_model = [0] * height
    next_grid_model = [0] * height
    for i in range(0, width):
        grid_model[i] = [0] * width
        next_grid_model[i] = [0] * width


def reset_model():
    """set all cells to 0"""
    global grid_model
    for i in range(0, height):
        for j in range(0, width):
            grid_model[i][j] = "0"


def get_neighbours(row, column):
    """calculate living neighbours around a cell
    specified by its coordinates"""
    global grid_model
    count = 0
    if column - 1 >= 0:
        count += int(grid_model[row][column - 1])
    if column - 1 >= 0 and row - 1 >= 0:
        count += int(grid_model[row - 1][column - 1])
    if row - 1 >= 0:
        count += int(grid_model[row - 1][column])
    if column + 1 < width and row - 1 >= 0:
        count += int(grid_model[row - 1][column + 1])
    if column + 1 < width:
        count += int(grid_model[row][column + 1])
    if column + 1 < width and row + 1 < height:
        count += int(grid_model[row + 1][column + 1])
    if row + 1 < height:
        count += int(grid_model[row + 1][column])
    if column - 1 >= 0 and row + 1 < height:
        count += int(grid_model[row + 1][column - 1])

    return count


def get_next_generation():
    """calculate cells' state based on the game rules"""
    global grid_model, next_grid_model

    for i in range(0, height):
        for j in range(0, width):
            new_state = "0"
            neighbours = get_neighbours(i, j)
            if grid_model[i][j] == "1" and (neighbours == 2 or neighbours == 3):
                new_state = "1"
            else:
                if neighbours == 3:
                    new_state = "1"
            next_grid_model[i][j] = new_state

    temp = grid_model  # swap model and next_grid_model so you are not updating the model you are counting living cells in
    grid_model = next_grid_model  # next_grid_model is the future state of the model based on current model's state
    next_grid_model = temp


def seed_random():
    """seed the grid model randomly"""
    global grid_model
    for i in range(0, height):
        for j in range(0, width):
            grid_model[i][j] = str(random.randint(0, 1))


def stringify_pattern():
    """reads grid_model's state and saves it into a string that is returned"""
    global grid_model
    text = ""
    for i in range(0, height):
        for j in range(0, width):
            text += str(grid_model[i][j])
        text += '\n'
    return text


def read_pattern_file(file):
    """reads text file with a pattern into grid_model"""
    reset_model()
    for i in range(0, height):
        line = file.readline()
        for j in range(0, width):
            if line[j] != '\n':
                grid_model[i][j] = line[j]


# two pre-set patterns
glider_pattern = [[0, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0],
                  [0, 0, 0, 1, 0],
                  [0, 1, 1, 1, 0],
                  [0, 0, 0, 0, 0]]

glider_gun_pattern = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                      [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


def load_pattern(pattern, xoffset=0, yoffset=0):
    """reads pre-set patterns into grid_model"""
    global grid_model
    reset_model()
    for i in range(0, len(pattern)):  # number of rows
        for j in range(0, len(pattern[0])):  # number of columns
            grid_model[xoffset + i][yoffset + j] = str(pattern[i][j])


if __name__ == "__main__":
    create_grid()
    get_next_generation()

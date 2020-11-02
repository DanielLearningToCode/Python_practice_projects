"""Implementation of John Conway's Game of Life
Modified and extended version of the project in Head First
Learn to Code by Eric Freeman
To run the game run the view.py file"""

from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfile
import os
import model

cell_size = 5
is_running = False


def setup():
    """creates GUI"""
    global cell_size, root, grid_view, start_button, clear_button, choice
    root = Tk()  # create tkinter window/screen
    root.title("The game of life")
    # create cavas inside the main window (root)
    grid_view = Canvas(root, width=model.width * cell_size,
                       height=model.height * cell_size,
                       borderwidth=0, highlightthickness=0,
                       bg="white")
    # set layout manager to grid. Set the canvas to upper part of the window, the whole width. Add padding
    grid_view.grid(row=0, columnspan=5, padx=20, pady=20)
    # register the canvas with event handler (grid_handler). Event triggered by left mouse
    grid_view.bind("<Button-1>", grid_handler)

    # StringVar is object to store options given as strings
    # selected option is stored in StringVar (choice).
    choice = StringVar(root)
    choice.set('Choose a Pattern')
    # create dropdown menu = OptionMenu inside the window (root).
    # command = event-handler method
    option = OptionMenu(root, choice, "random", "glider", "glider_gun", "load from file", command=option_handler)
    option.config(width=20)
    option.grid(row=1, column=1, padx=20)
    start_button = Button(root, text="Start", width=12)
    clear_button = Button(root, text="Clear", width=12)
    start_button.grid(row=1, column=0, sticky=W, padx=20, pady=20)  # sticky=W  is float left (West)
    start_button.bind("<Button-1>", start_handler)
    clear_button.grid(row=1, column=2, padx=20, pady=20)
    clear_button.bind("<Button-1>", clear_handler)
    save_button = Button(root, text="Save", width=12, command=save_pattern)  # command=method is an alternative to
    # .bind()
    save_button.grid(row=1, column=4, sticky=E, padx=20, pady=20)


def option_handler(event):
    """selects action based on the chosen action in OptionMenu widget"""
    global is_running, start_button
    start_button.configure(text="Start")
    is_running = False
    if choice.get() == "random":
        model.seed_random()
    elif choice.get() == "glider":
        model.load_pattern(model.glider_pattern, 10, 10)
    elif choice.get() == "glider_gun":
        model.load_pattern(model.glider_gun_pattern, 10, 10)
    elif choice.get() == "load from file":
        load_file()
    update()


def start_handler(event):
    """starts the loop"""
    global is_running, start_button
    if is_running:
        start_button.configure(text="Start")
        is_running = False
    else:
        start_button.configure(text="Pause")
        is_running = True
        update()


def clear_handler(event):
    """sets to all grid_model cells to 0 and clears the grid_view (screen)"""
    global is_running, start_button
    start_button.configure(text="Start")
    is_running = False
    model.reset_model()
    update()


def grid_handler(event):
    """reads the x and y coordinates of the mouse
    click iside grid_view (screen) and switches cell's state"""
    col = int(event.x / cell_size)
    row = int(event.y / cell_size)
    if model.grid_model[row][col] == "1":
        model.grid_model[row][col] = "0"
        draw_cell(row, col, "white")
    else:
        model.grid_model[row][col] = "1"
        draw_cell(row, col, "black")


def save_pattern():
    """displays save file dialog to save the pattern currently on the screen"""
    file = asksaveasfile(mode="w", defaultextension=".txt",
                         initialdir=os.getcwd())  # os.getcwd = get current working directory
    if file is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save = model.stringify_pattern()
    file.write(text2save)
    file.close()


def load_file():
    """displays open file dialog to select a text file with the pattern to load"""
    file = askopenfile(initialdir=os.getcwd())
    if file is not None:
        model.read_pattern_file(file)


def update():
    """reads grid_model and updates grid_view (screen) accordingly"""
    global grid_view, root, is_running
    if is_running:
        root.after(100, update)
        model.get_next_generation()
    grid_view.delete(ALL)

    for i in range(0, model.height):
        for j in range(0, model.width):
            if model.grid_model[i][j] == "1":
                draw_cell(i, j, "black")


def draw_cell(row, col, color):
    """draws a single cell on the grid_view (screen) based on arguments"""
    global grid_view
    outline = "gray" if color == "black" else "white"  # python ternary operator
    grid_view.create_rectangle(col * cell_size, row * cell_size,
                               col * cell_size + cell_size,
                               row * cell_size + cell_size,
                               outline=outline, fill=color)


if __name__ == "__main__":
    model.create_grid()
    setup()
    update()
    mainloop()

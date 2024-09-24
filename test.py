import turtle
from tkinter import Tk, Text, Button, Label, Entry
import zipfile
import json
import os

# Initialize the main screen
screen = turtle.Screen()
screen.title("Color Grid Application")
screen.setup(width=800, height=800)
screen.tracer(0)

GRID_AREA_HEIGHT = 700
grid_size = 0
block_size = 50
block_colors = {}  # To store the colors of blocks
action_history = []

grid_turtle = turtle.Turtle()
grid_turtle.hideturtle()
grid_turtle.penup()
grid_turtle.speed(0)

history_turtle = turtle.Turtle()
history_turtle.hideturtle()
history_turtle.penup()
history_turtle.speed(0)

# Tkinter window setup
root = Tk()
root.title("Grid Color Application")
root.geometry("800x300")

# Text box to accept user input for commands
command_box = Text(root, height=2, width=60)
command_box.grid(row=0, column=0, columnspan=4)

# Labels for row/column entry
row_label = Label(root, text="Row Number:")
row_label.grid(row=1, column=0)
row_entry = Entry(root)
row_entry.grid(row=1, column=1)

column_label = Label(root, text="Column Number:")
column_label.grid(row=2, column=0)
column_entry = Entry(root)
column_entry.grid(row=2, column=1)

# Function to get the grid size
def get_grid_size():
    num = screen.numinput("Grid Size", "Enter an odd number of blocks (e.g., 3, 5, 7):", default=5, minval=1, maxval=21)
    return int(num) if num and num % 2 == 1 else 5

# Function to draw the grid
def draw_grid(blocks):
    global block_size, grid_size
    grid_size = blocks
    block_size = GRID_AREA_HEIGHT / blocks

    grid_turtle.clear()
    start_x = -GRID_AREA_HEIGHT / 2
    start_y = GRID_AREA_HEIGHT / 2

    for row in range(blocks):
        for col in range(blocks):
            x = start_x + col * block_size
            y = start_y - row * block_size
            draw_square(x, y, block_size, 'black', 'white')
            block_num = row * blocks + col + 1
            grid_turtle.goto(x + block_size / 2, y - block_size - 20)
            grid_turtle.write(str(block_num), align="center", font=("Arial", 12, "normal"))
    
    screen.update()

# Function to draw a square with a specific color
def draw_square(x, y, size, outline_color, fill_color):
    grid_turtle.goto(x, y)
    grid_turtle.pendown()
    grid_turtle.color(outline_color, fill_color)
    grid_turtle.begin_fill()
    for _ in range(4):
        grid_turtle.forward(size)
        grid_turtle.right(90)
    grid_turtle.end_fill()
    grid_turtle.penup()

# Function to color a block with a specific color
def color_block(block_num, color):
    global block_colors
    try:
        block_num = int(block_num)  # Ensure block_num is an integer
        if not (1 <= block_num <= grid_size * grid_size):
            return
        
        row = (block_num - 1) // grid_size
        col = (block_num - 1) % grid_size

        x = -GRID_AREA_HEIGHT / 2 + col * block_size
        y = GRID_AREA_HEIGHT / 2 - row * block_size

        color_hex = convert_color(color)
        if color_hex:  # Only draw if the color is valid
            draw_square(x, y, block_size, 'black', color_hex)
            block_colors[block_num] = color_hex
            action_history.append((block_num, color_hex))
            update_history_display()
            screen.update()
    except ValueError:
        print("Invalid block number.")

# Function to update the history display
def update_history_display():
    history_turtle.clear()
    history_turtle.goto(-380, GRID_AREA_HEIGHT / 2 + 20)
    if action_history:
        history_text = "History: " + ", ".join([f"{num}{color}" for num, color in action_history])
    else:
        history_text = "History: None"
    history_turtle.write(history_text, align="left", font=("Arial", 12, "normal"))

# Process the command entered in the text box
def process_command():
    command = command_box.get("1.0", "end").strip().lower()

    if command.startswith("fill"):
        parts = command.split()
        if len(parts) >= 4 and parts[1].isdigit() and parts[2] == "with":
            block_num = parts[1]  # Keep it as a string to convert later
            color_input = " ".join(parts[3:])
            color_block(block_num, color_input)
    
    command_box.delete("1.0", "end")

# Function to fill an entire row
def fill_row():
    try:
        row = int(row_entry.get())
        color = command_box.get("1.0", "end").strip()
        if 1 <= row <= grid_size:
            for col in range(1, grid_size + 1):
                block_num = (row - 1) * grid_size + col
                color_block(block_num, color)
    except ValueError:
        print("Invalid row number.")
    command_box.delete("1.0", "end")

# Function to fill an entire column
def fill_column():
    try:
        column = int(column_entry.get())
        color = command_box.get("1.0", "end").strip()
        if 1 <= column <= grid_size:
            for row in range(1, grid_size + 1):
                block_num = (row - 1) * grid_size + column
                color_block(block_num, color)
    except ValueError:
        print("Invalid column number.")
    command_box.delete("1.0", "end")

# Function to convert color inputs
def convert_color(color_input):
    color_input = color_input.strip().lower()
    
    # Check for plaintext color names
    if color_input in {'red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'black', 'white', 'gray', 'purple', 'orange'}:
        return color_input
    
    # Check for hexadecimal
    if color_input.startswith('#') and len(color_input) == 7:
        return color_input
    
    # Check for RGB tuple
    if color_input.startswith('(') and color_input.endswith(')'):
        try:
            rgb_values = tuple(map(int, color_input[1:-1].split(',')))
            if len(rgb_values) == 3 and all(0 <= v <= 255 for v in rgb_values):
                # Convert RGB to hex
                return f'#{rgb_values[0]:02x}{rgb_values[1]:02x}{rgb_values[2]:02x}'
        except ValueError:
            pass  # Ignore invalid RGB input

    return None  # Return None for invalid inputs

# Save grid to a zip file
def save_grid():
    grid_data = {
        'grid_size': grid_size,
        'block_colors': block_colors,
    }
    
    # Save grid data to a JSON file
    with open('grid_data.json', 'w') as f:
        json.dump(grid_data, f)
    
    # Zip the file
    with zipfile.ZipFile('grid.zip', 'w') as zf:
        zf.write('grid_data.json')
    
    # Remove the JSON file after zipping
    os.remove('grid_data.json')

# Load grid from a zip file
def load_grid():
    if not os.path.exists('grid.zip'):
        return  # Handle case where file does not exist
    
    # Unzip and load the grid data
    with zipfile.ZipFile('grid.zip', 'r') as zf:
        zf.extractall()

    with open('grid_data.json', 'r') as f:
        grid_data = json.load(f)
    
    os.remove('grid_data.json')  # Clean up extracted file

    # Restore grid size and block colors
    global grid_size, block_colors
    grid_size = grid_data['grid_size']
    block_colors = grid_data['block_colors']

    # Redraw the grid
    draw_grid(grid_size)
    
    # Recolor the blocks
    for block_num, color in block_colors.items():
        color_block(block_num, color)

# Reset the grid
def reset_grid():
    global action_history, block_colors, grid_size
    action_history = []
    block_colors = {}
    grid_turtle.clear()
    history_turtle.clear()
    grid_size = get_grid_size()
    draw_grid(grid_size)
    update_history_display()
    screen.update()

# Buttons to handle various commands
submit_button = Button(root, text="Submit Command", command=process_command)
submit_button.grid(row=0, column=3)

fill_row_button = Button(root, text="Fill Row", command=fill_row)
fill_row_button.grid(row=1, column=2)

fill_column_button = Button(root, text="Fill Column", command=fill_column)
fill_column_button.grid(row=2, column=2)

save_button = Button(root, text="Save Grid", command=save_grid)
save_button.grid(row=3, column=0)

load_button = Button(root, text="Load Grid", command=load_grid)
load_button.grid(row=3, column=1)

reset_button = Button(root, text="Reset Grid", command=reset_grid)
reset_button.grid(row=3, column=2)

# Initial setup
grid_size = get_grid_size()
draw_grid(grid_size)
update_history_display()

# Start the main loop
turtle.mainloop()
root.mainloop()

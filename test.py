import turtle

# Initialize the main screen
screen = turtle.Screen()
screen.title("Color Grid Application")
screen.setup(width=800, height=800)  # Fixed window size
screen.tracer(0)  # Turn off automatic updating for smoother drawing

# Define areas:
# - Grid Area: Bottom 700 pixels
# - History Area: Top 100 pixels

GRID_AREA_HEIGHT = 700
HISTORY_AREA_HEIGHT = 100

# Create turtles
grid_turtle = turtle.Turtle()
grid_turtle.hideturtle()
grid_turtle.penup()
grid_turtle.speed(0)

history_turtle = turtle.Turtle()
history_turtle.hideturtle()
history_turtle.penup()
history_turtle.speed(0)

# Define colors
colors = {
    'r': 'red',
    'o': 'orange',
    'y': 'yellow',
    'g': 'green',
    'b': 'blue',
    'i': 'indigo',
    'v': 'violet'
}

# Variables to track state
grid_size = 0
block_size = 50
input_buffer = ""
action_history = []  # List of tuples: (block_num, color_key)
block_colors = {}  # Mapping of block_num to color_key

# Function to get an odd number for grid size
def get_grid_size():
    while True:
        num = screen.numinput("Grid Size", "Enter an odd number of blocks (e.g., 3, 5, 7):", default=5, minval=1, maxval=21)
        if num is None:
            continue  # Prompt again if input is cancelled
        num = int(num)
        if num % 2 == 1:
            return num
        else:
            screen.textinput("Invalid Input", "Please enter an odd number.")

# Function to draw the grid
def draw_grid(blocks):
    global block_size, grid_size
    grid_size = blocks
    block_size = GRID_AREA_HEIGHT / blocks  # Adjust block size to fit the grid area

    grid_turtle.clear()

    start_x = -GRID_AREA_HEIGHT / 2
    start_y = GRID_AREA_HEIGHT / 2

    for row in range(blocks):
        for col in range(blocks):
            x = start_x + col * block_size
            y = start_y - row * block_size
            draw_square(x, y, block_size, outline_color='black', fill_color='white')
            # Write the block number below the square
            block_num = row * blocks + col + 1
            grid_turtle.goto(x + block_size / 2, y - block_size - 20)
            grid_turtle.write(str(block_num), align="center", font=("Arial", 12, "normal"))

    screen.update()

# Function to draw a single square
def draw_square(x, y, size, outline_color='black', fill_color='white'):
    grid_turtle.goto(x, y)
    grid_turtle.pendown()
    grid_turtle.color(outline_color, fill_color)
    grid_turtle.begin_fill()
    for _ in range(4):
        grid_turtle.forward(size)
        grid_turtle.right(90)
    grid_turtle.end_fill()
    grid_turtle.penup()

# Function to color a specific block
def color_block(block_num, color_key):
    global block_colors
    if color_key not in colors:
        return  # Invalid color key

    if not (1 <= block_num <= grid_size * grid_size):
        return  # Invalid block number

    # Calculate row and column
    row = (block_num - 1) // grid_size
    col = (block_num - 1) % grid_size

    # Calculate position
    x = -GRID_AREA_HEIGHT / 2 + col * block_size
    y = GRID_AREA_HEIGHT / 2 - row * block_size

    # Draw filled square with color
    draw_square(x, y, block_size, outline_color='black', fill_color=colors[color_key])

    # Update block_colors and action_history
    block_colors[block_num] = color_key
    action_history.append((block_num, color_key))

    # Update history display
    update_history_display()

    screen.update()

# Function to update the history display
def update_history_display():
    history_turtle.clear()
    history_turtle.goto(-380, GRID_AREA_HEIGHT / 2 + 20)  # Position in history area
    if action_history:
        history_text = "History: " + ", ".join([f"{num}{color}" for num, color in action_history])
    else:
        history_text = "History: None"
    history_turtle.write(history_text, align="left", font=("Arial", 12, "normal"))

# Function to process the input buffer
def process_input():
    global input_buffer
    if len(input_buffer) < 2:
        input_buffer = ""  # Not enough characters
        return

    # Extract block number and color key
    block_part = input_buffer[:-1]
    color_key = input_buffer[-1].lower()

    if not block_part.isdigit() or color_key not in colors:
        input_buffer = ""  # Invalid input
        return

    block_num = int(block_part)

    if 1 <= block_num <= grid_size * grid_size:
        color_block(block_num, color_key)
    else:
        # Invalid block number, optionally display a message
        pass

    input_buffer = ""  # Reset buffer after processing

# Function to handle key presses
def handle_keypress(key):
    global input_buffer

    if key in colors:
        # If a color key is pressed, process the current input buffer
        input_buffer += key
        process_input()
    elif key.isdigit():
        # If a number key is pressed, add to the buffer
        input_buffer += key
    elif key == 'u':
        # Undo the last action
        undo_last_action()
    elif key == 'x':  # Changed from 'r' to 'x' for reset
        # Reset the grid
        reset_grid()
    # Ignore other keys

# Function to undo the last action
def undo_last_action():
    if not action_history:
        return  # Nothing to undo

    last_block, last_color = action_history.pop()
    block_colors.pop(last_block, None)

    # Reset the block to white
    row = (last_block - 1) // grid_size
    col = (last_block - 1) % grid_size
    x = -GRID_AREA_HEIGHT / 2 + col * block_size
    y = GRID_AREA_HEIGHT / 2 - row * block_size
    draw_square(x, y, block_size, outline_color='black', fill_color='white')

    update_history_display()
    screen.update()

# Function to reset the grid
def reset_grid():
    global action_history, block_colors, input_buffer, grid_size
    action_history = []
    block_colors = {}
    input_buffer = ""
    grid_turtle.clear()
    history_turtle.clear()
    grid_size = get_grid_size()  # Get new grid size
    draw_grid(grid_size)  # Redraw the grid with new size
    update_history_display()
    bind_keys()  # Rebind keys after resetting
    screen.update()

# Function to display the current input in the history area
def display_current_input():
    history_turtle.goto(-380, GRID_AREA_HEIGHT / 2 + 50)  # Position above history text
    history_turtle.write(f"Current Input: {input_buffer}", align="left", font=("Arial", 12, "normal"))

# Initial setup
def setup():
    global grid_size
    grid_size = get_grid_size()
    draw_grid(grid_size)
    update_history_display()

# Bind key presses
def bind_keys():
    # Clear existing key bindings
    screen._root.bind_all('<KeyPress>', lambda e: None)

    # Bind digits 0-9
    for digit in '0123456789':
        screen.onkey(lambda d=digit: handle_keypress(d), digit)
    
    # Bind color keys (r, o, y, g, b, i, v)
    for color_key in colors.keys():
        screen.onkey(lambda c=color_key: handle_keypress(c), color_key)
    
    # Bind undo (u) and reset (x)
    screen.onkey(lambda: handle_keypress('u'), 'u')  # Undo
    screen.onkey(lambda: handle_keypress('x'), 'x')  # Reset

    screen.listen()

# Run the application
setup()
bind_keys()
screen.mainloop()

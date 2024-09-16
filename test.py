import turtle

# Set up turtle screen
screen = turtle.Screen()
speed(0)
screen = turtle.Screen()
screen.setup(width=1000, height=1000, startx=498, starty=498)

# Separate turtle for writing input on screen
input_turtle = turtle.Turtle()
input_turtle.penup()
input_turtle.hideturtle()

# Colors corresponding to ROYGBIV
colors = {'r': 'red', 'o': 'orange', 'y': 'yellow', 'g': 'green', 'b': 'blue', 'i': 'indigo', 'v': 'violet'}

# Variables to track the selected block and color
selected_block = None
grid_size = 0
input_buffer = ''  # Buffer to collect multi-digit inputs
block_size = 50  # Default block size

# Function to draw a grid
def draw_grid(blocks):
    global grid_size, block_size
    grid_size = blocks
    window_width = screen.window_width()
    window_height = screen.window_height()
    
    # Adjust block size based on window size
    block_size = min(window_width, window_height) // blocks
    
    t.penup()
    start_x = -(blocks // 2) * block_size
    start_y = (blocks // 2) * block_size
    for row in range(blocks):
        for col in range(blocks):
            draw_square(start_x + col * block_size, start_y - row * block_size)
    t.hideturtle()

# Function to draw a square
def draw_square(x, y):
    t.goto(x, y)
    t.pendown()
    for _ in range(4):
        t.forward(block_size)
        t.right(90)
    t.penup()

# Function to color a specific block
def color_block(block_num, color):
    global grid_size
    row = (block_num - 1) // grid_size  # Determine the row of the block
    col = (block_num - 1) % grid_size  # Determine the column of the block
    start_x = -((grid_size // 2) * block_size)  # Calculate start_x based on grid size
    start_y = (grid_size // 2) * block_size  # Calculate start_y based on grid size
    
    t.penup()
    # Correct coordinates for turtle movement
    t.goto(start_x + col * block_size, start_y - row * block_size)
    
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(4):
        t.forward(block_size)
        t.right(90)
    t.end_fill()

# Function to process selected block from buffer
def select_block():
    global selected_block, input_buffer
    if input_buffer.isdigit():
        block_num = int(input_buffer)
        if 1 <= block_num <= grid_size * grid_size:
            selected_block = block_num
            print(f"Selected block: {selected_block}")
        else:
            print(f"Invalid block number. Please enter a block between 1 and {grid_size * grid_size}")
    input_buffer = ''  # Reset the buffer after processing the input

# Function to handle number key presses (0-9)
def handle_number_key(digit):
    global input_buffer
    input_buffer += digit
    print(f"Current input: {input_buffer}")
    display_input()  # Call to update the displayed input

# Function to listen for a color key press and color the selected block
def color_selected_block(color_key):
    global selected_block
    if input_buffer:
        select_block()  # Process the buffered number before coloring
    if selected_block is not None and color_key in colors:
        color_block(selected_block, colors[color_key])
        print(f"Colored block {selected_block} {colors[color_key]}")
        selected_block = None  # Reset selection after coloring
        display_input()  # Update the display to clear input after action

# Function to display the current input under the grid
def display_input():
    input_turtle.clear()  # Clear previous input before writing the new one
    input_turtle.goto(-screen.window_width() // 2 + 20, -screen.window_height() // 2 + 20)  # Set position under the grid
    input_turtle.write(f"Input: {input_buffer}", align="center", font=("Arial", 12, "normal"))

# Input validation for odd number
def get_odd_input():
    while True:
        num = turtle.numinput("Grid Size", "Enter the number of blocks (odd number):", default=3, minval=1, maxval=101)
        if num is None:
            return None
        if int(num) % 2 == 1:
            return int(num)
        else:
            turtle.textinput("Error", "Please enter an odd number.")

# Main program
def main():
    blocks = get_odd_input()
    if blocks:
        draw_grid(blocks)

    # Bind number keys to handle multi-digit input
    for i in range(10):
        screen.onkey(lambda i=i: handle_number_key(str(i)), str(i))

    # Bind ROYGBIV keys to color the selected block
    screen.onkey(lambda: color_selected_block('r'), 'r')
    screen.onkey(lambda: color_selected_block('o'), 'o')
    screen.onkey(lambda: color_selected_block('y'), 'y')
    screen.onkey(lambda: color_selected_block('g'), 'g')
    screen.onkey(lambda: color_selected_block('b'), 'b')
    screen.onkey(lambda: color_selected_block('i'), 'i')
    screen.onkey(lambda: color_selected_block('v'), 'v')

    screen.listen()

    # Prevent the window from closing immediately
    turtle.done()
    screen.mainloop()

if __name__ == "__main__":
    main()


import turtle

# Set up turtle screen
screen = turtle.Screen()
screen.title("Grid Drawing")
t = turtle.Turtle()
t.speed(0)

# Colors corresponding to ROYGBIV
colors = {'r': 'red', 'o': 'orange', 'y': 'yellow', 'g': 'green', 'b': 'blue', 'i': 'indigo', 'v': 'violet'}

# Function to draw a grid
def draw_grid(blocks):
    t.penup()
    start_x = -((blocks // 2) * 50)
    start_y = (blocks // 2) * 50
    for row in range(blocks):
        for col in range(blocks):
            draw_square(start_x + col * 50, start_y - row * 50)
    t.hideturtle()

# Function to draw a square
def draw_square(x, y):
    t.goto(x, y)
    t.pendown()
    for _ in range(4):
        t.forward(50)
        t.right(90)
    t.penup()

# Function to color a specific block
def color_block(block_num, blocks, color):
    row = (block_num - 1) // blocks
    col = (block_num - 1) % blocks
    start_x = -((blocks // 2) * 50)
    start_y = (blocks // 2) * 50
    t.penup()
    # Adjust Y-coordinate to fix the top row issue
    t.goto(start_x + col * 50 + 1, start_y - row * 50 - 49)
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(4):
        t.forward(48)
        t.right(90)
    t.end_fill()

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

        while True:
            user_input = turtle.textinput("Color Block", "Enter a block number and color (e.g., 32r) or 'q' to quit:")
            if user_input is None or user_input.lower() == 'q':
                break
            user_input = user_input.lower()

            if len(user_input) >= 2 and user_input[:-1].isdigit() and user_input[-1] in colors:
                block_num = int(user_input[:-1])
                if 1 <= block_num <= blocks * blocks:
                    color_block(block_num, blocks, colors[user_input[-1]])
                else:
                    turtle.textinput("Error", f"Please enter a block number between 1 and {blocks * blocks}.")
            else:
                turtle.textinput("Error", "Invalid input. Try again.")

    # Prevent the window from closing immediately
    turtle.done()
    screen.mainloop()  # Keep the window open until the user manually closes it

if __name__ == "__main__":
    main()

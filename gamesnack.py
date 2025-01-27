import tkinter
import random

ROWS = 25
COLS = 25
SIZE = 25
WINDOW_WIDTH = SIZE*ROWS
WINDOW_HEIGHT = SIZE*COLS
INITIAL_SPEED = 100

class tile:
    def __init__(self, x, y):
        self.x=x
        self.y=y

#game window

window = tkinter.Tk()
window.title("Snack Game")
window.resizable(False,False)

canvas = tkinter.Canvas(window,bg='black',width=WINDOW_WIDTH,height=WINDOW_HEIGHT,borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

#center the window
WINDOW_WIDTH=window.winfo_width()
WINDOW_HEIGHT=window.winfo_height()
screen_width=window.winfo_screenwidth()
screen_height=window.winfo_screenheight()

window_x = int((screen_width/2)-(WINDOW_WIDTH/2))
window_y = int((screen_height/2)-(WINDOW_HEIGHT/2))

window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{window_x}+{window_y}")

#initialize game
snake = tile(5*SIZE,5*SIZE)  #single tile for the snake head
food = tile(10*SIZE,10*SIZE)

snake_body=[]
velocityX=0
velocityY=0
game_over = False
score = 0
speed = INITIAL_SPEED
def reset_game():
    """Reset all game variables to restart the game."""
    global snake, food, snake_body, velocityX, velocityY, game_over, score, speed
    snake = tile(5 * SIZE, 5 * SIZE)
    food = tile(10 * SIZE, 10 * SIZE)
    snake_body = []
    velocityX = 0
    velocityY = 0
    game_over = False
    score = 0
    speed = INITIAL_SPEED
    draw()  # Restart the draw loop

def change_direction(e):                 #e=event
    
    #print(e.keysym)
    global velocityX, velocityY, game_over
    if (game_over):
        return

    if(e.keysym =="Up" and velocityY != 1):
        velocityX=0
        velocityY=-1
    elif(e.keysym =="Down" and velocityY !=-1):
        velocityX=0
        velocityY=1
    elif(e.keysym =="Left" and velocityX != 1):
        velocityX=-1
        velocityY=0
    elif(e.keysym =="Right" and velocityX != -1):
        velocityX=1
        velocityY=0

def move():
    global snake, food, snake_body, game_over, score
    if game_over:
        return

    # Check if the snake hits the wall
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return

    # Check if the snake collides with its own body
    for body_part in snake_body:
        if snake.x == body_part.x and snake.y == body_part.y:
            game_over = True
            return

    # Check for collision with food
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(tile(food.x, food.y))
        food.x = random.randint(0, COLS - 1) * SIZE
        food.y = random.randint(0, ROWS - 1) * SIZE
        score += 1

    # Update snake's body
    for i in range(len(snake_body) - 1, 0, -1):
        snake_body[i].x = snake_body[i - 1].x
        snake_body[i].y = snake_body[i - 1].y

    if len(snake_body) > 0:
        snake_body[0].x = snake.x
        snake_body[0].y = snake.y

    # Move the snake's head
    snake.x += velocityX * SIZE
    snake.y += velocityY * SIZE


def draw():
    global snake, food, snake_body, game_over, score
    move()
    canvas.delete('all')

    #food
    canvas.create_rectangle(food.x,food.y,food.x + SIZE,food.y + SIZE, fill= "red"  )

    #drawing snake
    canvas.create_rectangle(snake.x,snake.y,snake.x + SIZE, snake.y + SIZE, fill = "lime green")
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y,tile.x + SIZE,tile.y + SIZE, fill = "lime green")

    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20", text=f"Game Over: {score}", fill="white")

    else:
        canvas.create_text(30,20, font="Arial 10", text=f"score:{score}",fill = "white")
    window.after(speed, draw)

window.bind("<KeyRelease>", change_direction)  #Bind keys


# start game
draw()
window.mainloop()
import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.resizable(False, False)

        # Game constants
        self.GAME_WIDTH = 700
        self.GAME_HEIGHT = 500
        self.SPEED = 150
        self.SPACE_SIZE = 20
        self.BODY_PARTS = 3
        self.SNAKE_COLOR = "#00FF00"
        self.FOOD_COLOR = "#FF0000"
        self.BACKGROUND_COLOR = "#000000"

        # Game variables
        self.direction = 'right'
        self.score = 0
        
        # Create score label
        self.label = tk.Label(self.master, text=f"Score: {self.score}", font=('consolas', 40))
        self.label.pack()

        # Create game canvas
        self.canvas = tk.Canvas(
            self.master, 
            bg=self.BACKGROUND_COLOR,
            height=self.GAME_HEIGHT,
            width=self.GAME_WIDTH
        )
        self.canvas.pack()

        # Initialize snake and food
        self.snake_positions = []
        self.food_position = []
        self.snake_body = []
        
        # Bind arrow keys
        self.master.bind('<Left>', lambda event: self.change_direction('left'))
        self.master.bind('<Right>', lambda event: self.change_direction('right'))
        self.master.bind('<Up>', lambda event: self.change_direction('up'))
        self.master.bind('<Down>', lambda event: self.change_direction('down'))

        # Center the window
        self.center_window()
        
        # Start game
        self.start_game()

    def center_window(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width/2) - (self.GAME_WIDTH/2)
        y = (screen_height/2) - (self.GAME_HEIGHT/2)
        self.master.geometry(f'{self.GAME_WIDTH}x{self.GAME_HEIGHT+50}+{int(x)}+{int(y)}')

    def start_game(self):
        # Create snake
        for i in range(self.BODY_PARTS):
            x = self.SPACE_SIZE * (self.BODY_PARTS - i)
            y = self.SPACE_SIZE
            self.snake_positions.append([x, y])
            square = self.canvas.create_rectangle(
                x, y,
                x + self.SPACE_SIZE, y + self.SPACE_SIZE,
                fill=self.SNAKE_COLOR, tag="snake"
            )
            self.snake_body.append(square)

        # Create food
        self.spawn_food()
        
        # Start game loop
        self.next_turn()

    def spawn_food(self):
        if self.food_position:
            self.canvas.delete("food")

        x = random.randint(0, (self.GAME_WIDTH // self.SPACE_SIZE) - 1) * self.SPACE_SIZE
        y = random.randint(0, (self.GAME_HEIGHT // self.SPACE_SIZE) - 1) * self.SPACE_SIZE
        self.food_position = [x, y]
        
        self.canvas.create_oval(
            x, y,
            x + self.SPACE_SIZE, y + self.SPACE_SIZE,
            fill=self.FOOD_COLOR, tag="food"
        )

    def next_turn(self):
        # Get current head position
        head_x, head_y = self.snake_positions[0]

        # Update position based on direction
        if self.direction == "left":
            head_x -= self.SPACE_SIZE
        elif self.direction == "right":
            head_x += self.SPACE_SIZE
        elif self.direction == "up":
            head_y -= self.SPACE_SIZE
        elif self.direction == "down":
            head_y += self.SPACE_SIZE

        # Insert new head position
        self.snake_positions.insert(0, [head_x, head_y])
        
        # Create new square for head
        square = self.canvas.create_rectangle(
            head_x, head_y,
            head_x + self.SPACE_SIZE, head_y + self.SPACE_SIZE,
            fill=self.SNAKE_COLOR
        )
        self.snake_body.insert(0, square)

        # Check if food is eaten
        if head_x == self.food_position[0] and head_y == self.food_position[1]:
            self.score += 1
            self.label.config(text=f"Score: {self.score}")
            self.spawn_food()
        else:
            # Remove tail
            del self.snake_positions[-1]
            self.canvas.delete(self.snake_body[-1])
            del self.snake_body[-1]

        # Check for collision
        if self.check_collisions():
            self.game_over()
        else:
            self.master.after(self.SPEED, self.next_turn)

    def check_collisions(self):
        head_x, head_y = self.snake_positions[0]

        # Check wall collision
        if head_x < 0 or head_x >= self.GAME_WIDTH:
            return True
        if head_y < 0 or head_y >= self.GAME_HEIGHT:
            return True

        # Check self collision
        if [head_x, head_y] in self.snake_positions[1:]:
            return True

        return False

    def game_over(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(
            self.canvas.winfo_width()/2,
            self.canvas.winfo_height()/2,
            font=('consolas', 70),
            text=f"GAME OVER\nScore: {self.score}",
            fill="red",
            justify=tk.CENTER
        )

    def change_direction(self, new_direction):
        if (new_direction == 'left' and self.direction != 'right' or
            new_direction == 'right' and self.direction != 'left' or
            new_direction == 'up' and self.direction != 'down' or
            new_direction == 'down' and self.direction != 'up'):
            self.direction = new_direction

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
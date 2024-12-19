import tkinter as tk
import random

class PingPongGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping Pong")
        
        # Game settings
        self.canvas_width = 800
        self.canvas_height = 400
        self.paddle_speed = 20
        self.ball_speed_x = 4
        self.ball_speed_y = 4
        self.paddle_width = 20
        self.paddle_height = 100
        self.ball_size = 20
        
        # Create canvas
        self.canvas = tk.Canvas(
            root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg='black'
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Create paddles
        self.left_paddle = self.canvas.create_rectangle(
            50, self.canvas_height/2 - self.paddle_height/2,
            50 + self.paddle_width, self.canvas_height/2 + self.paddle_height/2,
            fill='white'
        )
        
        self.right_paddle = self.canvas.create_rectangle(
            self.canvas_width - 50 - self.paddle_width, self.canvas_height/2 - self.paddle_height/2,
            self.canvas_width - 50, self.canvas_height/2 + self.paddle_height/2,
            fill='white'
        )
        
        # Create ball
        self.ball = self.canvas.create_oval(
            self.canvas_width/2 - self.ball_size/2, self.canvas_height/2 - self.ball_size/2,
            self.canvas_width/2 + self.ball_size/2, self.canvas_height/2 + self.ball_size/2,
            fill='white'
        )
        
        # Create scores
        self.score_left = 0
        self.score_right = 0
        self.score_display = self.canvas.create_text(
            self.canvas_width/2, 50,
            text=f"{self.score_left} - {self.score_right}",
            fill='white',
            font=('Arial', 20)
        )
        
        # Create center line
        for i in range(0, self.canvas_height, 30):
            self.canvas.create_line(
                self.canvas_width/2, i,
                self.canvas_width/2, i + 15,
                fill='white',
                width=2
            )
        
        # Bind keys
        self.root.bind('<w>', lambda e: self.move_paddle(self.left_paddle, -self.paddle_speed))
        self.root.bind('<s>', lambda e: self.move_paddle(self.left_paddle, self.paddle_speed))
        self.root.bind('<Up>', lambda e: self.move_paddle(self.right_paddle, -self.paddle_speed))
        self.root.bind('<Down>', lambda e: self.move_paddle(self.right_paddle, self.paddle_speed))
        
        # Game state
        self.game_running = False
        
        # Create start button
        self.start_button = tk.Button(
            root,
            text="Start Game",
            command=self.start_game
        )
        self.start_button.pack(pady=5)
        
        # Add instructions
        self.instructions = tk.Label(
            root,
            text="Left Player: W/S    Right Player: ↑/↓",
            font=('Arial', 12)
        )
        self.instructions.pack(pady=5)

    def move_paddle(self, paddle, dy):
        # Get current paddle position
        pos = self.canvas.coords(paddle)
        
        # Check boundaries
        if (pos[1] + dy >= 0 and pos[3] + dy <= self.canvas_height):
            self.canvas.move(paddle, 0, dy)

    def reset_ball(self):
        # Move ball to center
        self.canvas.coords(
            self.ball,
            self.canvas_width/2 - self.ball_size/2,
            self.canvas_height/2 - self.ball_size/2,
            self.canvas_width/2 + self.ball_size/2,
            self.canvas_height/2 + self.ball_size/2
        )
        
        # Randomize initial direction
        self.ball_speed_x = 4 * random.choice([-1, 1])
        self.ball_speed_y = 4 * random.choice([-1, 1])

    def update_score(self):
        self.canvas.itemconfig(
            self.score_display,
            text=f"{self.score_left} - {self.score_right}"
        )

    def check_collision(self):
        ball_pos = self.canvas.coords(self.ball)
        left_paddle_pos = self.canvas.coords(self.left_paddle)
        right_paddle_pos = self.canvas.coords(self.right_paddle)
        
        # Ball hits top or bottom
        if ball_pos[1] <= 0 or ball_pos[3] >= self.canvas_height:
            self.ball_speed_y = -self.ball_speed_y
        
        # Ball hits left paddle
        if (ball_pos[0] <= left_paddle_pos[2] and
            ball_pos[2] >= left_paddle_pos[0] and
            ball_pos[1] <= left_paddle_pos[3] and
            ball_pos[3] >= left_paddle_pos[1]):
            self.ball_speed_x = abs(self.ball_speed_x)  # Move right
            self.increase_speed()
        
        # Ball hits right paddle
        if (ball_pos[2] >= right_paddle_pos[0] and
            ball_pos[0] <= right_paddle_pos[2] and
            ball_pos[1] <= right_paddle_pos[3] and
            ball_pos[3] >= right_paddle_pos[1]):
            self.ball_speed_x = -abs(self.ball_speed_x)  # Move left
            self.increase_speed()
        
        # Ball goes out
        if ball_pos[0] <= 0:
            self.score_right += 1
            self.update_score()
            self.reset_ball()
        elif ball_pos[2] >= self.canvas_width:
            self.score_left += 1
            self.update_score()
            self.reset_ball()

    def increase_speed(self):
        # Increase ball speed slightly after each paddle hit
        self.ball_speed_x *= 1.05
        self.ball_speed_y *= 1.05

    def update(self):
        if self.game_running:
            self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)
            self.check_collision()
            self.root.after(16, self.update)  # Update every 16ms (roughly 60 FPS)

    def start_game(self):
        if not self.game_running:
            self.game_running = True
            self.reset_ball()
            self.update()
            self.start_button.config(text="Restart Game")
        else:
            self.score_left = 0
            self.score_right = 0
            self.update_score()
            self.reset_ball()

if __name__ == "__main__":
    root = tk.Tk()
    game = PingPongGame(root)
    root.mainloop()
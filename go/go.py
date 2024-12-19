import tkinter as tk
from tkinter import messagebox

class GomokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Gomoku")
        
        # Game settings
        self.board_size = 15
        self.cell_size = 40
        self.current_player = "Black"
        self.board = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # Create canvas
        canvas_size = self.board_size * self.cell_size
        self.canvas = tk.Canvas(
            root, 
            width=canvas_size, 
            height=canvas_size, 
            background='#DEB887'
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Draw board
        self.draw_board()
        
        # Bind click event
        self.canvas.bind('<Button-1>', self.handle_click)
        
        # Create status label
        self.status_label = tk.Label(
            root, 
            text=f"Current Player: {self.current_player}",
            font=('Arial', 12)
        )
        self.status_label.pack(pady=5)
        
        # Create reset button
        self.reset_button = tk.Button(
            root, 
            text="Reset Game", 
            command=self.reset_game
        )
        self.reset_button.pack(pady=5)

    def draw_board(self):
        # Draw lines
        for i in range(self.board_size):
            # Vertical lines
            self.canvas.create_line(
                i * self.cell_size + self.cell_size/2, 
                self.cell_size/2,
                i * self.cell_size + self.cell_size/2, 
                self.board_size * self.cell_size - self.cell_size/2,
                fill='black'
            )
            # Horizontal lines
            self.canvas.create_line(
                self.cell_size/2, 
                i * self.cell_size + self.cell_size/2,
                self.board_size * self.cell_size - self.cell_size/2, 
                i * self.cell_size + self.cell_size/2,
                fill='black'
            )

    def handle_click(self, event):
        # Convert click coordinates to board position
        col = int((event.x - self.cell_size/2) // self.cell_size)
        row = int((event.y - self.cell_size/2) // self.cell_size)
        
        # Check if position is valid and empty
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if self.board[row][col] == '':
                # Place stone
                self.place_stone(row, col)
                
                # Check for win
                if self.check_win(row, col):
                    messagebox.showinfo("Game Over", f"{self.current_player} wins!")
                    self.reset_game()
                else:
                    # Switch player
                    self.current_player = "White" if self.current_player == "Black" else "Black"
                    self.status_label.config(text=f"Current Player: {self.current_player}")

    def place_stone(self, row, col):
        # Calculate position
        x = col * self.cell_size + self.cell_size/2
        y = row * self.cell_size + self.cell_size/2
        
        # Draw stone
        color = 'black' if self.current_player == "Black" else 'white'
        self.canvas.create_oval(
            x - self.cell_size/3,
            y - self.cell_size/3,
            x + self.cell_size/3,
            y + self.cell_size/3,
            fill=color,
            outline='black'
        )
        
        # Update board state
        self.board[row][col] = self.current_player

    def check_win(self, row, col):
        # Directions to check (horizontal, vertical, diagonal)
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1  # Count the current stone
            
            # Check in positive direction
            r, c = row + dr, col + dc
            while (0 <= r < self.board_size and 
                   0 <= c < self.board_size and 
                   self.board[r][c] == self.current_player):
                count += 1
                r += dr
                c += dc
            
            # Check in negative direction
            r, c = row - dr, col - dc
            while (0 <= r < self.board_size and 
                   0 <= c < self.board_size and 
                   self.board[r][c] == self.current_player):
                count += 1
                r -= dr
                c -= dc
            
            if count >= 5:
                return True
        
        return False

    def reset_game(self):
        # Clear board state
        self.board = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Redraw board
        self.draw_board()
        
        # Reset player
        self.current_player = "Black"
        self.status_label.config(text=f"Current Player: {self.current_player}")

if __name__ == "__main__":
    root = tk.Tk()
    game = GomokuGame(root)
    root.mainloop()
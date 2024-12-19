import tkinter as tk
from tkinter import messagebox, ttk
import random 

class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        
        # Create settings frame
        self.settings_frame = tk.Frame(self.master)
        self.settings_frame.pack(pady=5)
        
        # Create mine count selector
        tk.Label(
            self.settings_frame,
            text="Number of Mines:",
            font=('Arial', 12)
        ).pack(side=tk.LEFT, padx=5)
        
        self.mine_var = tk.StringVar(value="15")
        self.mine_entry = ttk.Spinbox(
            self.settings_frame,
            from_=1,
            to=99,
            width=5,
            textvariable=self.mine_var
        )
        self.mine_entry.pack(side=tk.LEFT, padx=5)
        
        # Create restart button
        self.restart_button = tk.Button(
            self.settings_frame,
            text="Restart Game",
            command=self.restart_game
        )
        self.restart_button.pack(side=tk.LEFT, padx=10)
        
        # Game settings
        self.rows = 10
        self.cols = 10
        self.cell_size = 30
        
        self.setup_new_game()

    def setup_new_game(self):
        # Get number of mines from entry
        try:
            self.mines = min(int(self.mine_var.get()), self.rows * self.cols - 1)
            self.mine_var.set(str(self.mines))  # Update display if number was reduced
        except ValueError:
            self.mines = 15
            self.mine_var.set("15")
        
        # Game state
        self.cells = {}
        self.mine_locations = set()
        self.revealed = set()
        self.flags = set()
        self.game_over = False
        
        # Create or clear the game board
        if hasattr(self, 'game_frame'):
            self.game_frame.destroy()
        
        # Create the game board
        self.create_board()
        self.place_mines()
        
        # Bind right-click
        self.master.bind('<Button-3>', self.on_right_click)

    def create_board(self):
        # Create game frame
        self.game_frame = tk.Frame(
            self.master,
            bd=3,
            relief=tk.SUNKEN
        )
        self.game_frame.pack(padx=10, pady=10)
        
        # Create cells
        for i in range(self.rows):
            for j in range(self.cols):
                cell = tk.Button(
                    self.game_frame,
                    width=2,
                    height=1,
                    command=lambda row=i, col=j: self.on_click(row, col)
                )
                cell.grid(row=i, column=j)
                self.cells[(i, j)] = cell

        # Create mine counter
        if hasattr(self, 'mine_label'):
            self.mine_label.destroy()
            
        self.mine_label = tk.Label(
            self.master,
            text=f"Mines: {self.mines}",
            font=('Arial', 16)
        )
        self.mine_label.pack(pady=5)

    def place_mines(self):
        # Randomly place mines
        positions = [(i, j) for i in range(self.rows) for j in range(self.cols)]
        self.mine_locations = set(random.sample(positions, self.mines))

    def get_neighbors(self, row, col):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row, new_col = row + i, col + j
                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    neighbors.append((new_row, new_col))
        return neighbors

    def count_adjacent_mines(self, row, col):
        count = 0
        for neighbor in self.get_neighbors(row, col):
            if neighbor in self.mine_locations:
                count += 1
        return count

    def on_click(self, row, col):
        if self.game_over:
            return
        
        if (row, col) in self.flags:
            return
        
        if (row, col) in self.mine_locations:
            self.game_over = True
            self.reveal_all_mines()
            messagebox.showinfo("Game Over", "You hit a mine!")
            return
        
        self.reveal_cell(row, col)
        
        if len(self.revealed) + len(self.mine_locations) == self.rows * self.cols:
            self.game_over = True
            messagebox.showinfo("Congratulations", "You won!")

    def reveal_cell(self, row, col):
        if (row, col) in self.revealed:
            return
        
        self.revealed.add((row, col))
        
        # Count adjacent mines
        adjacent_mines = self.count_adjacent_mines(row, col)
        
        # Update button appearance
        button = self.cells[(row, col)]
        button.config(relief=tk.SUNKEN)
        
        if adjacent_mines > 0:
            # Show number of adjacent mines
            colors = ['blue', 'green', 'red', 'purple', 'maroon', 'turquoise', 'black', 'gray']
            button.config(text=str(adjacent_mines), fg=colors[adjacent_mines-1])
        else:
            # If no adjacent mines, reveal neighbors
            button.config(bg='lightgray')
            for neighbor in self.get_neighbors(row, col):
                if neighbor not in self.revealed:
                    self.reveal_cell(*neighbor)

    def on_right_click(self, event):
        if self.game_over:
            return
        
        # Get the widget under cursor
        widget = event.widget.winfo_containing(event.x_root, event.y_root)
        
        # Find the cell coordinates
        for (row, col), cell in self.cells.items():
            if cell == widget:
                if (row, col) in self.revealed:
                    return
                
                if (row, col) in self.flags:
                    # Remove flag
                    self.flags.remove((row, col))
                    cell.config(text='', bg='SystemButtonFace')
                else:
                    # Add flag
                    self.flags.add((row, col))
                    cell.config(text='🚩', bg='yellow')
                
                # Update mine counter
                self.mine_label.config(text=f"Mines: {self.mines - len(self.flags)}")
                break

    def reveal_all_mines(self):
        for row, col in self.mine_locations:
            button = self.cells[(row, col)]
            button.config(text='💣', bg='red')

    def restart_game(self):
        self.setup_new_game()

def new_game():
    root = tk.Tk()
    game = Minesweeper(root)
    return root

if __name__ == "__main__":
    root = new_game()
    root.mainloop()
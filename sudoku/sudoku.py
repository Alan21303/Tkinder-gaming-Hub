import tkinter as tk
from tkinter import messagebox
import random

class SudokuGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku")
        self.cells = {}
        self.selected = None
        self.original_numbers = set()  # Track initial numbers that shouldn't be modified
        self.solving_in_progress = False
        
        # Create the game board
        self.create_board()
        
        # Create control buttons
        self.create_controls()
        
        # Initialize the game
        self.new_game()

    def create_board(self):
        # Create main game grid
        self.game_frame = tk.Frame(
            self.master,
            bd=3,
            relief=tk.SOLID
        )
        self.game_frame.pack(padx=10, pady=10)

        # Create 9x9 grid of entry cells
        for i in range(9):
            for j in range(9):
                cell_frame = tk.Frame(
                    self.game_frame,
                    borderwidth=1,
                    relief=tk.SOLID,
                    width=50,
                    height=50
                )
                cell_frame.grid(row=i, column=j, padx=1, pady=1)
                cell_frame.grid_propagate(False)
                cell_label = tk.Label(
                    cell_frame,
                    text="",
                    font=('Arial', 18),
                    justify=tk.CENTER
                )
                cell_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                
                # Add thick borders for 3x3 sub-grids
                if i in [3, 6]:
                    cell_frame.grid(pady=(3, 1))
                if j in [3, 6]:
                    cell_frame.grid(padx=(3, 1))
                
                self.cells[(i, j)] = {
                    'label': cell_label,
                    'frame': cell_frame,
                    'value': 0
                }
                
                # Bind click event
                cell_frame.bind('<Button-1>', lambda e, i=i, j=j: self.cell_clicked(i, j))
                cell_label.bind('<Button-1>', lambda e, i=i, j=j: self.cell_clicked(i, j))

        # Bind number keys
        self.master.bind('<Key>', self.key_pressed)

    def create_controls(self):
        control_frame = tk.Frame(self.master)
        control_frame.pack(pady=10)
        
        tk.Button(
            control_frame,
            text="New Game",
            command=self.new_game
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame,
            text="Solve",
            command=self.start_solve
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame,
            text="Check",
            command=self.check_solution
        ).pack(side=tk.LEFT, padx=5)

    def cell_clicked(self, i, j):
        if self.solving_in_progress:
            return
            
        # Deselect previous cell
        if self.selected:
            old_i, old_j = self.selected
            self.cells[(old_i, old_j)]['frame'].configure(bg='white')
        
        # Select new cell if it's not an original number
        if (i, j) not in self.original_numbers:
            self.selected = (i, j)
            self.cells[(i, j)]['frame'].configure(bg='lightblue')
        else:
            self.selected = None

    def key_pressed(self, event):
        if self.solving_in_progress:
            return
            
        if self.selected and event.char in '123456789':
            i, j = self.selected
            if (i, j) not in self.original_numbers:
                self.cells[(i, j)]['value'] = int(event.char)
                self.cells[(i, j)]['label'].configure(text=event.char)
        elif event.char == '0' or event.char == ' ':  # Clear cell
            if self.selected and self.selected not in self.original_numbers:
                i, j = self.selected
                self.cells[(i, j)]['value'] = 0
                self.cells[(i, j)]['label'].configure(text='')

    def new_game(self):
        self.solving_in_progress = False
        # Clear the board
        self.original_numbers.clear()
        for i in range(9):
            for j in range(9):
                self.cells[(i, j)]['value'] = 0
                self.cells[(i, j)]['label'].configure(text='')
                self.cells[(i, j)]['frame'].configure(bg='white')
        
        # Generate a new puzzle
        self.generate_puzzle()

    def generate_puzzle(self):
        # Start with a solved board
        base = 3
        side = base * base

        # Pattern for a baseline valid solution
        def pattern(r, c):
            return (base * (r % base) + r // base + c) % side

        # Randomize rows, columns and numbers (of valid base pattern)
        def shuffle(s): 
            return random.sample(s, len(s))

        rBase = range(base)
        rows  = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols  = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums  = shuffle(range(1, base * base + 1))

        # Produce board using randomized baseline pattern
        board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        # Remove some numbers to create the puzzle
        squares = side * side
        empties = squares * 3//4
        for p in random.sample(range(squares), empties):
            board[p // side][p % side] = 0

        # Fill the board
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    self.cells[(i, j)]['value'] = board[i][j]
                    self.cells[(i, j)]['label'].configure(text=str(board[i][j]))
                    self.original_numbers.add((i, j))

    def is_valid(self, num, pos):
        # Check row
        for j in range(9):
            if self.cells[(pos[0], j)]['value'] == num and pos[1] != j:
                return False

        # Check column
        for i in range(9):
            if self.cells[(i, pos[1])]['value'] == num and pos[0] != i:
                return False

        # Check 3x3 box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.cells[(i, j)]['value'] == num and (i, j) != pos:
                    return False

        return True

    def start_solve(self):
        self.solving_in_progress = True
        # Clear user-filled cells before starting the recursive solve
        for i in range(9):
            for j in range(9):
                if (i, j) not in self.original_numbers:
                    self.cells[(i, j)]['value'] = 0
                    self.cells[(i, j)]['label'].configure(text='')
        # Start the recursive solving process
        self.solve_game()
        self.solving_in_progress = False

    def solve_game(self):
        find = self.find_empty()
        if not find:
            return True
        
        row, col = find
        for num in range(1, 10):
            if self.is_valid(num, (row, col)):
                self.cells[(row, col)]['value'] = num
                self.cells[(row, col)]['label'].configure(text=str(num))
                self.master.update()
                
                if self.solve_game():
                    return True
                
                self.cells[(row, col)]['value'] = 0
                self.cells[(row, col)]['label'].configure(text='')
                self.master.update()
        
        return False

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.cells[(i, j)]['value'] == 0:
                    return (i, j)
        return None

    def check_solution(self):
        if self.solving_in_progress:
            return
            
        # Check if the board is filled
        if self.find_empty():
            messagebox.showinfo("Incomplete", "Please fill in all cells!")
            return

        # Check if the solution is valid
        for i in range(9):
            for j in range(9):
                num = self.cells[(i, j)]['value']
                self.cells[(i, j)]['value'] = 0
                if not self.is_valid(num, (i, j)):
                    self.cells[(i, j)]['value'] = num
                    messagebox.showinfo("Incorrect", "The solution is not valid!")
                    return
                self.cells[(i, j)]['value'] = num

        messagebox.showinfo("Congratulations!", "You solved the puzzle correctly!")

if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()
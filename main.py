import tkinter as tk
from tkinter import ttk
import os
import subprocess
from PIL import Image, ImageTk

class GameLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Launcher")
        self.root.geometry("800x600")
        self.root.configure(bg='#2C3E50')

        # Game directories and their corresponding main files
        self.games = {
            "Go Game": {"dir": "go", "main": "go.py"},
            "Minesweeper": {"dir": "mine", "main": "mine.py"},
            "Ping Pong": {"dir": "pingpong", "main": "pingpong.py"},
            "SnakeGame": {"dir": "snakegame", "main": "snake.py"},
            "Sudoku": {"dir": "sudoku", "main": "sudoku.py"}
        }

        self.create_widgets()

    def create_widgets(self):
        # Create main frame
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Title Label
        title_label = tk.Label(
            main_frame,
            text="Game Center",
            font=('Helvetica', 24, 'bold'),
            bg='#2C3E50',
            fg='white'
        )
        title_label.pack(pady=20)

        # Create frame for game buttons
        games_frame = tk.Frame(main_frame, bg='#2C3E50')
        games_frame.pack(expand=True, fill='both')

        # Configure grid
        for i in range(2):
            games_frame.grid_columnconfigure(i, weight=1)

        # Create game buttons
        row = 0
        col = 0
        for game_name in self.games:
            self.create_game_button(games_frame, game_name, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

        # Exit button
        exit_button = tk.Button(
            main_frame,
            text="Exit",
            command=self.root.quit,
            font=('Helvetica', 12),
            bg='#E74C3C',
            fg='white',
            width=20,
            height=2
        )
        exit_button.pack(pady=20)

    def create_game_button(self, parent, game_name, row, col):
        # Create frame for each game
        game_frame = tk.Frame(
            parent,
            bg='#34495E',
            padx=10,
            pady=10,
            relief=tk.RAISED,
            borderwidth=2
        )
        game_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # Game name label
        name_label = tk.Label(
            game_frame,
            text=game_name,
            font=('Helvetica', 14, 'bold'),
            bg='#34495E',
            fg='white'
        )
        name_label.pack(pady=5)

        # Launch button
        launch_button = tk.Button(
            game_frame,
            text="Launch Game",
            command=lambda g=game_name: self.launch_game(g),
            bg='#3498DB',
            fg='white',
            font=('Helvetica', 10),
            width=15,
            height=2
        )
        launch_button.pack(pady=10)

    def launch_game(self, game_name):
        game_info = self.games[game_name]
        game_dir = game_info["dir"]
        main_file = game_info["main"]

        # Get the current directory
        current_dir = os.getcwd()
        
        # Construct the full path to the game
        game_path = os.path.join(current_dir, game_dir, main_file)

        try:
            # Launch the game using Python
            subprocess.Popen(['python', game_path])
        except Exception as e:
            error_message = f"Error launching {game_name}:\n{str(e)}"
            tk.messagebox.showerror("Error", error_message)

def main():
    root = tk.Tk()
    app = GameLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
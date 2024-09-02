import os
import sys
import random
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def supports_color():
    # Check if the terminal supports colors
    if sys.platform == 'win32':
        return os.system("") == 0
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

colors_enabled = supports_color()

colors = {
    'reset': Style.RESET_ALL if colors_enabled else '',
    'red': Fore.RED if colors_enabled else '',
    'green': Fore.GREEN if colors_enabled else '',
    'yellow': Fore.YELLOW if colors_enabled else '',
    'blue': Fore.BLUE if colors_enabled else '',
    'cyan': Fore.CYAN if colors_enabled else '',
    'white': Fore.WHITE if colors_enabled else '',
    'mine': Fore.RED if colors_enabled else '',
    'flag': Fore.MAGENTA if colors_enabled else '',
    'number': {
        1: Fore.BLUE if colors_enabled else '',
        2: Fore.GREEN if colors_enabled else '',
        3: Fore.RED if colors_enabled else '',
        4: Fore.CYAN if colors_enabled else '',
        5: Fore.YELLOW if colors_enabled else '',
        6: Fore.MAGENTA if colors_enabled else '',
        7: Fore.WHITE if colors_enabled else '',
        8: Fore.LIGHTBLACK_EX if colors_enabled else '',
    }
}

# Constants for the game
SIZE = 12  # Size of the grid (12x12)
MINES_COUNT = 25  # Number of mines on the board

class Cell:
    def __init__(self, x, y, is_mine=False):
        self.x = x  # Row position
        self.y = y  # Column position
        self.is_mine = is_mine  # Whether the cell is a mine
        self.is_revealed = False  # Whether the cell has been revealed
        self.is_flagged = False  # Whether the cell has been flagged
        self.adjacent_mines = 0  # Number of adjacent mines

class Minesweeper:
    def __init__(self):
        self.board = [[Cell(x, y) for y in range(SIZE)] for x in range(SIZE)]
        self.game_over = False
        self.victory = False
        self.first_move = True  # To ensure first move is never a mine
        self.remaining_cells = SIZE * SIZE - MINES_COUNT  # Cells to reveal to win

    def generate_mines(self, initial_x, initial_y):
        mines_placed = 0
        while mines_placed < MINES_COUNT:
            x = random.randint(0, SIZE - 1)
            y = random.randint(0, SIZE - 1)
            cell = self.board[x][y]
            # Ensure the first move is not a mine and no duplicate mines
            if not cell.is_mine and (x != initial_x or y != initial_y):
                cell.is_mine = True
                mines_placed += 1
        self.calculate_adjacent_mines()

    def calculate_adjacent_mines(self):
        for x in range(SIZE):
            for y in range(SIZE):
                cell = self.board[x][y]
                if cell.is_mine:
                    continue
                adjacent = self.get_adjacent_cells(x, y)
                cell.adjacent_mines = sum(1 for c in adjacent if c.is_mine)

    def get_adjacent_cells(self, x, y):
        adjacent = []
        for i in range(max(0, x - 1), min(SIZE, x + 2)):
            for j in range(max(0, y - 1), min(SIZE, y + 2)):
                if i == x and j == y:
                    continue
                adjacent.append(self.board[i][j])
        return adjacent

    def reveal_cell(self, x, y):
        cell = self.board[x][y]
        if cell.is_revealed or cell.is_flagged:
            return
        cell.is_revealed = True

        if cell.is_mine:
            self.game_over = True
            self.victory = False
        else:
            self.remaining_cells -= 1
            if cell.adjacent_mines == 0:
                for adj in self.get_adjacent_cells(x, y):
                    if not adj.is_revealed:
                        self.reveal_cell(adj.x, adj.y)
            if self.remaining_cells == 0:
                self.game_over = True
                self.victory = True

    def flag_cell(self, x, y):
        cell = self.board[x][y]
        if cell.is_revealed:
            return
        cell.is_flagged = not cell.is_flagged

    def print_board(self):
        print("    " + " ".join(f"{i:2}" for i in range(SIZE)))
        print("   " + "---" * SIZE)
        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                cell = self.board[i][j]
                if cell.is_revealed:
                    if cell.is_mine:
                        cell_repr = colors['mine'] + "* " + colors['reset']
                    elif cell.adjacent_mines > 0:
                        cell_repr = colors['number'][cell.adjacent_mines] + f"{cell.adjacent_mines} " + colors['reset']
                    else:
                        cell_repr = "  "  # Empty cell
                elif cell.is_flagged:
                    cell_repr = colors['flag'] + "F " + colors['reset']
                else:
                    cell_repr = "# "
                row.append(cell_repr)
            print(f"{i:2} | " + " ".join(row))
        print()

    def start_game(self):
        print("Welcome to Minesweeper!")
        print(f"Uncover all cells without mines to win. Board size: {SIZE}x{SIZE}, Mines: {MINES_COUNT}")
        while not self.game_over:
            self.print_board()
            try:
                action, x, y = self.get_player_input()
                if self.first_move:
                    self.generate_mines(x, y)
                    self.first_move = False
                if action == 'r':
                    self.reveal_cell(x, y)
                elif action == 'f':
                    self.flag_cell(x, y)
                else:
                    print("Invalid action. Use 'r' to reveal and 'f' to flag.")
            except Exception as e:
                print(f"Error: {e}")
                print("Invalid input. Please enter action and coordinates correctly.")

        self.print_board()
        if self.victory:
            print("Congratulations! You cleared all the mines!")
            print("Here is your reward link: http://lockwoodsideology.com")
        else:
            print("Boom! You hit a mine. Game over.")
            self.restart_prompt()

    def get_player_input(self):
        user_input = input("Enter your move (e.g., 'r 3 4' to reveal cell at row 3, column 4): ")
        parts = user_input.strip().split()
        if len(parts) != 3:
            raise ValueError("Input must be in the format: action x y")
        action = parts[0].lower()
        x = int(parts[1])
        y = int(parts[2])
        if action not in ('r', 'f'):
            raise ValueError("Action must be 'r' (reveal) or 'f' (flag).")
        if not (0 <= x < SIZE and 0 <= y < SIZE):
            raise ValueError(f"Coordinates must be between 0 and {SIZE - 1}.")
        return action, x, y

    def restart_prompt(self):
        choice = input("Would you like to play again? (y/n): ").strip().lower()
        if choice == 'y':
            self.__init__()
            self.start_game()
        else:
            print("Thank you for playing!")
            sys.exit()

if __name__ == "__main__":
    game = Minesweeper()
    game.start_game()

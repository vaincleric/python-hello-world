from http.server import BaseHTTPRequestHandler
import os
import sys
import random
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def supports_color():
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

SIZE = 12
MINES_COUNT = 25

class Cell:
    def __init__(self, x, y, is_mine=False):
        self.x = x
        self.y = y
        self.is_mine = is_mine
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

class Minesweeper:
    def __init__(self):
        self.board = [[Cell(x, y) for y in range(SIZE)] for x in range(SIZE)]
        self.game_over = False
        self.victory = False
        self.first_move = True
        self.remaining_cells = SIZE * SIZE - MINES_COUNT

    def generate_mines(self, initial_x, initial_y):
        mines_placed = 0
        while mines_placed < MINES_COUNT:
            x = random.randint(0, SIZE - 1)
            y = random.randint(0, SIZE - 1)
            cell = self.board[x][y]
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
        output = []
        output.append("    " + " ".join(f"{i:2}" for i in range(SIZE)))
        output.append("   " + "---" * SIZE)
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
                        cell_repr = "  "
                elif cell.is_flagged:
                    cell_repr = colors['flag'] + "F " + colors['reset']
                else:
                    cell_repr = "# "
                row.append(cell_repr)
            output.append(f"{i:2} | " + " ".join(row))
        return "\n".join(output)

    def start_game(self):
        if self.victory:
            return "Congratulations! You cleared all the mines!\nHere is your reward link: http://lockwoodsideology.com"
        elif self.game_over:
            return "Boom! You hit a mine. Game over.\n"

class handler(BaseHTTPRequestHandler):
    game = Minesweeper()

    def do_GET(self):
        if self.game.first_move:
            self.game.generate_mines(0, 0)  # Placeholder for actual player move
            self.game.first_move = False
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        response = self.game.print_board() + self.game.start_game()
        self.wfile.write(response.encode('utf-8'))

if __name__ == "__main__":
    from http.server import HTTPServer
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, handler)
    print("Starting server at http://localhost:8000")
    httpd.serve_forever()

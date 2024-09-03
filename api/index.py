from http.server import BaseHTTPRequestHandler

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        cell = Cell(0, 0)
        response = f"Cell created at position ({cell.x}, {cell.y})"
        self.wfile.write(response.encode('utf-8'))
        return

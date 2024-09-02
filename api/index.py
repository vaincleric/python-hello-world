from http.server import BaseHTTPRequestHandler, HTTPServer

class Minesweeper:
    def print_board(self):
        return "Sample Board"

class handler(BaseHTTPRequestHandler):
    game = Minesweeper()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        response = self.game.print_board()
        self.wfile.write(response.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=handler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting http server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()

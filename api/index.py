from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    game = Minesweeper()

    def do_GET(self):
        # Parse the query string
        parsed_path = urlparse(self.path)
        query = parse_qs(parsed_path.query)

        action = query.get('action', [None])[0]
        x = query.get('x', [None])[0]
        y = query.get('y', [None])[0]

        if action and x is not None and y is not None:
            x = int(x)
            y = int(y)
            if action == 'r':
                self.game.reveal_cell(x, y)
            elif action == 'f':
                self.game.flag_cell(x, y)

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

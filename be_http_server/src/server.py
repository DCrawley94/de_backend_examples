from http.server import BaseHTTPRequestHandler, HTTPServer
from db.connection import conn

import json


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/games':
            # Get Data and columns
            query_result = conn.run("SELECT * FROM games;")
            # could also hardcode this
            games_columns = [col['name'] for col in conn.columns]

            # Use column names to format data - this is to turn it into list
            #   of dictionaries rather than list of lists - can be skipped over
            formatted_games_data = []

            for game in query_result:
                game = {games_columns[i]: game[i]
                        for i in range(len(games_columns))}
                formatted_games_data.append(game)

            # prepare response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            # prepare response body
            data = json.dumps({"games": formatted_games_data})

            # write body to response
            self.wfile.write(data.encode("utf-8"))


server_address = ('', 8000)
httpd = HTTPServer(server_address, Handler)
httpd.serve_forever()

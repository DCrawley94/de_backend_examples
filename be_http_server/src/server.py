from http.server import BaseHTTPRequestHandler, HTTPServer
from db.connection import connect_to_db
import json


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/games':
            conn = connect_to_db()
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

    def do_POST(self):
        if self.path == '/api/games':
            conn = connect_to_db()
            
            # This gets the size of data
            content_length = int(self.headers['Content-Length'])
            # This gets the data itself
            request_body = self.rfile.read(content_length).decode(
                'utf-8')

            # parse request body
            new_game = json.loads(request_body)

            insert_query_str = """
            INSERT INTO games
            (game_title, release_year, console_name, image_url)
            VALUES
            (:game_title, :release_year, :console_name, :image_url)
            RETURNING *;
            """

            inserted_game = conn.run(insert_query_str, **new_game)[0]

            # More formatting of data returned from the query
            game_columns = [col['name'] for col in conn.columns]
            formatted_game = {game_columns[i]: inserted_game[i]
                            for i in range(len(game_columns))}

            # prepare response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            # prepare response body
            data = json.dumps({"ride": formatted_game})

            # write body to response
            self.wfile.write(data.encode("utf-8"))


server_address = ('', 8000)
httpd = HTTPServer(server_address, Handler)
httpd.serve_forever()

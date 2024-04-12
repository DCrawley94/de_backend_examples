from fastapi import FastAPI, HTTPException
from db.connection import connect_to_db
from server_utils import format_response
from pg8000.exceptions import DatabaseError
from pydantic import BaseModel


class NewGame(BaseModel):
    game_title: str
    release_year: int
    console_name: str
    image_url: str


app = FastAPI()


@app.get('/api/reviews/{review_id}')
def get_review_by_id(review_id:int):
    conn = None
    try:
        conn = connect_to_db()
        query = """
        SELECT review_id, game_title, username, comment, rating 
        FROM reviews
        INNER JOIN games ON games.game_id = reviews.game_id
        WHERE review_id = :review_id;
        """

        review = conn.run(query, review_id=review_id)

        if not len(review):
            raise HTTPException(
                status_code=404, detail=f"No review found with id {review_id}"
            )

        columns = [col['name'] for col in conn.columns]
        response = format_response(columns, review, "review")

        return response
    except DatabaseError as db_error:
        # This error handling is only required if you're not relying on 
        #   pydantics 422s
        error = db_error.args[0]
        error_code = error['C']
        error_message = error['M']
        if error_code == '22P02':
            raise HTTPException(
                status_code=400, 
                detail=f"review_id should be an integer - {error_message}"
            )
    finally:
        if conn:
            conn.close()

@app.post('/api/games', status_code=201)
def post_game(new_game: NewGame):
    conn = None
    try:
        conn = connect_to_db()
        new_game = conn.run("""
        INSERT INTO games
        (game_title, release_year, console_name, image_url)
        VALUES
        (:game_title, :release_year, :console_name, :image_url)
        RETURNING *;
        """, **dict(new_game))
        columns = [col['name'] for col in conn.columns]
        response = format_response(columns, new_game, "game")
        return response
    finally:
        if conn:
            conn.close()
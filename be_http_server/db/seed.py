from db.connection import conn
from db.utils import create_games_lookup, format_reviews


def seed(games, reviews):
    # Drop tables
    conn.run("DROP TABLE IF EXISTS reviews;")
    conn.run("DROP TABLE IF EXISTS games;")

    # Create tables
    conn.run("""
    CREATE TABLE games (
            game_id SERIAL PRIMARY KEY,
            game_title VARCHAR NOT NULL,
            release_year INT,
            console_name VARCHAR NOT NULL,
            image_url VARCHAR
            );
    """)

    conn.run("""
    CREATE TABLE reviews (
            review_id SERIAL PRIMARY KEY,
            game_id INT NOT NULL REFERENCES games(game_id),
            username VARCHAR NOT NULL,
            comment VARCHAR NOT NULL,
            rating INT
            );
    """)

    # Insert Games
    inserted_games = []

    for game in games:
        insert_query = f"""
        INSERT INTO games
        (game_title, release_year, console_name, image_url)
        VALUES
        (
                '{game['game_title']}',
                {game['release_year']},
                '{game['console_name']}',
                '{game['image_url']}'
        )
        RETURNING *;
        """
        inserted_row = conn.run(insert_query)
        inserted_games.append(inserted_row[0])

    games_id_lookup = create_games_lookup(inserted_games)
    formatted_reviews = format_reviews(reviews, games_id_lookup)

    # Insert Reviews
    for review in formatted_reviews:
        insert_query = f"""
        INSERT INTO reviews
        (game_id, username, comment, rating)
        VALUES
        (
                {review['game_id']},
                '{review['username']}',
                '{review['comment']}',
                {review['rating']}
        )
        """

        conn.run(insert_query)

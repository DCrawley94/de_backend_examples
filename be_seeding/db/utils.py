from copy import deepcopy

def create_games_lookup(inserted_games):
    return {game[1]: game[0] for game in inserted_games}

def format_reviews(raw_reviews, games_id_lookup):
    """
    Accepts raw reviews data and replaces game title with a game_id
    """
    raw_reviews_copy = deepcopy(raw_reviews)

    for review in raw_reviews_copy:
        review['game_id'] = games_id_lookup[review['game_title']]
        del review['game_title']
    
    return raw_reviews_copy

def games_query_builder_example(games):
    """
    Arguments:
        data: list of dicts, each containing the data to insert for each row

    Returns:
        Constructed query string
    """


    base_query = """
    INSERT INTO games 
    (game_title, release_year, console_name, image_url)
    VALUES
    """

    rows_to_insert = ", ".join(
        f"('{game['game_title']}', '{game['release_year']}', '{game['console_name']}', '{game['image_url']}')" 
        for game in games)

    return base_query + rows_to_insert + " RETURNING *;"
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

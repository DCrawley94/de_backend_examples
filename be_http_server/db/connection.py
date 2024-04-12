import pg8000.native


def connect_to_db():
    return pg8000.native.Connection('YOUR_USERNAME', database="nc_games")

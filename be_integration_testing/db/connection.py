import pg8000.native

def connect_to_db():
    return pg8000.native.Connection('danika', database="nc_games")
from db.connection import conn 
from db.utils import create_games_lookup, format_reviews, games_query_builder_example
from pprint import pprint

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

	#  ~~~~~  SOLUTION WITHOUT QUERY BUILDER UTIL  ~~~~~  

	# Ready to collect inserted games for formatting reviews
	inserted_games = []

	# insert prepared games data - horrible for loop style
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
		# Note the quotation marks around the game title, console name and image url interpolated values
		#  If you don't have these it will lead to syntax errors

		inserted_row = conn.run(insert_query)
		inserted_games.append(inserted_row[0])

	# Create games_id lookup for formatting reviews
	games_id_lookup = create_games_lookup(inserted_games)
	
	# Format them to get game_id instead of game_title
	formatted_reviews = format_reviews(reviews, games_id_lookup)

	# insert prepared reviews data - another horrible for loop
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
	
	"""
	# ~~~~~  SOLUTION WITH QUERY BUILDER UTIL  ~~~~~

	# create query
	insert_games_query = games_query_builder_example(games)

	# run query to get games
	inserted_games = conn.run(insert_games_query)

	# Create games_id lookup for formatting reviews
	games_id_lookup = create_games_lookup(inserted_games)

	# etc..
	"""
	


from db.seed import seed
from db.data.index import data


try:
    seed(**data)
except Exception as e:
    print(e)

from config import config
import mongoengine


def connect_to_db(db_uri: str):
    mongoengine.connect(db_uri)

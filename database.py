import sqlite3
from sqlite3 import OperationalError
import config

def get_connection():
	return sqlite3.connect("database.db")

def check_for_errors_and_init():
	connection = get_connection()
	connection.execute(
			"CREATE TABLE IF NOT EXISTS categories ("
		        "id int NOT NULL UNIQUE, "
		        f"name varchar({config.max_category_length})"
			")"
	)

check_for_errors_and_init()
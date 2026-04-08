from app.database.db_management import SQLiteManagement


def add_user(username: str, password: str, email: str):
	with SQLiteManagement as db:
		db.
from app.database.db_management import SQLiteManagement
from typing import Optional, Sequence



def get_user_by_username(username: str) -> Optional[dict]:
	with SQLiteManagement() as db:
		query = "SELECT u.user_id, u.username, u.email FROM users u WHERE u.username = ?"

		data = db.query(query, (username,))
		return data[0] if data else None



def get_users() -> Optional[Sequence]:
	with SQLiteManagement() as db:
		query = "SELECT u.user_id, u.username, u.email FROM users u LIMIT 5"

		data = db.query(query)
		return data if data else None


def get_user_by_id(user_id: int) -> Optional[dict]:
	with SQLiteManagement() as db:
		query = "SELECT u.user_id, u.username, u.email FROM users u WHERE u.user_id = ?"

		data = db.query(query, (user_id, ))
		return data[0] if data else None


def add_user(username: str, password: str, email: str) -> Optional[dict]:
	with SQLiteManagement() as db:
		query = "INSERT INTO users('username', 'password', 'email') VALUES(?, ?, ?)"

		db.execute(query, (username, password, email))


def update_user_by_id(user_id: int, user_email: str) -> None:
	with SQLiteManagement() as db:
		query = "UPDATE users SET email = ? WHERE user_id = ?"
		db.execute(query, (user_email, user_id))


def delete_user_by_id(user_id: int) -> None:
	with SQLiteManagement() as db:
		query = "DELETE FROM users WHERE user_id = ?"
		db.execute(query, (user_id, ))


def is_valid_password(user_id: int, password: str) -> bool:
	with SQLiteManagement() as db:
		query = "SELECT u.user_id FROM users u WHERE u.user_id = ? AND u.password = ?"

		data = db.query(query, (user_id, password))
		return True if data else False
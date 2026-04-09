from app.database.db_management import SQLiteManagement
from typing import Optional


def get_user(username: str) -> Optional[dict]:
	with SQLiteManagement() as db:
		query = "SELECT u.user_id, u.username, u.email FROM users u WHERE u.username = ?"

		data = db.query(query, (username,))
		return data[0] if data else None

def is_valid_password(user_id: int, password: str) -> bool:
	with SQLiteManagement() as db:
		query = "SELECT u.user_id FROM users u WHERE u.user_id = ? AND u.password = ?"

		data = db.query(query, (user_id, password))
		return True if data else False
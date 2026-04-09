from app.database.db_management import SQLiteManagement
from typing import List, Dict


def get_token_by_jti(jti: str) -> Dict | None:
	with SQLiteManagement() as db:
		query = "SELECT jti, user_id, token_type, token, issued_at, expires_at, revoked FROM tokens WHERE jti = ?"

		response = db.query(query, (jti, ))

		return response[0] if response else None

def save_token(
	jti: str,
	user_id: int,
	issued_at: int,
	expires_at: int,
	token: str,
	token_type: str = "access_token",
	revoked: bool = False
) -> None:
	with SQLiteManagement() as db:
		query = "INSERT INTO tokens(jti, user_id, token_type, token, issued_at, expires_at, revoked) VALUES(?, ?, ?, ?, ?, ?, ?)"

		db.execute(query, (jti, user_id, token_type, token, issued_at, expires_at, revoked))
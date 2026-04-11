from app.database.db_management import SQLiteManagement
from typing import Dict, Sequence


def get_token_by_jti(jti: str) -> Dict | None:
	print("Recuperando token de la base de datos...", jti)
	with SQLiteManagement() as db:
		query = "SELECT jti, user_id, token_type, token, issued_at, expires_at, revoked FROM tokens WHERE jti = ?"

		response = db.query(query, (jti, ))

		return response[0] if response else None


def get_tokens_by_user(user_id: int) -> Sequence | None:
	print("Recuperando tokens del usuario", user_id)
	with SQLiteManagement() as db:
		query = "SELECT jti, user_id, token_type, token, issued_at, expires_at, revoked FROM tokens WHERE user_id = ?"

		response = db.query(query, (user_id, ))

		return response[0] if response else None


def revoke_token_by_jti(jti: str) -> None:
	print("Invalidando token...", jti)
	with SQLiteManagement() as db:
		query = "UPDATE tokens SET revoked = 1 WHERE jti = ?"
		db.execute(query, (jti, ))


def save_token(
	jti: str,
	user_id: int,
	issued_at: float,
	expires_at: float,
	token: str,
	token_type: str,
	revoked: bool = False
) -> None:
	with SQLiteManagement() as db:
		query = "INSERT INTO tokens(jti, user_id, token_type, token, issued_at, expires_at, revoked) VALUES(?, ?, ?, ?, ?, ?, ?)"

		db.execute(query, (jti, user_id, token_type, token, issued_at, expires_at, revoked))
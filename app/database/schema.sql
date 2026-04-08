-- Table for users create
CREATE TABLE IF NOT EXISTS users (
	user_id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT,
	password TEXT NOT NULL,
	email TEXT NOT NULL
);

-- Table for tracking refresh tokens and their revocation status
CREATE TABLE IF NOT EXISTS tokens (
	-- Unique token identifier (from JWT)
	jti TEXT PRIMARY KEY,

	-- Groups tokens from same login session
	family_id TEXT NOT NULL,

	-- Owner of the token
	user_id INTEGER NOT NULL,

	-- User-Agent for session management UI
	device_info TEXT,

	-- When token was issued
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	-- When token becomes invalid
	expires_at TIMESTAMP NOT NULL,

	-- Whether token has been invalidated
	revoked BOOLEAN DEFAULT FALSE,

	CONSTRAINT fk_tokens_users FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS estimations (
	estimation_id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	input TEXT NOT NULL,
	estimation TEXT NOT NULL,


	CONSTRAINT fk_estimations_users FOREIGN KEY (user_id) REFERENCES users(user_id)
);
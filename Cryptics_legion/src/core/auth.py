# src/core/auth.py
import bcrypt
from core import db

# register: uses db.insert_user
def register_user(username: str, password: str) -> bool:
    if not username or not password:
        return False
    pw_blob = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return db.insert_user(username, pw_blob)


# login: verify against hashed blob
def login_user(username: str, password: str):
    if not username or not password:
        return None
    row = db.get_user_by_username(username)
    if not row:
        return None
    user_id, pw_blob = row[0], row[1]
    if isinstance(pw_blob, str):
        pw_blob = pw_blob.encode("utf-8")
    if bcrypt.checkpw(password.encode("utf-8"), pw_blob):
        return user_id
    return None

from datetime import datetime, timedelta
from jose import jwt
import bcrypt

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

# Hash a password using bcrypt
def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(
        bytes(password, encoding="utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")

# Verify a password using bcrypt
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        bytes(plain_password, encoding="utf-8"),
        bytes(hashed_password, encoding="utf-8"),
    )

# Create a JWT token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    print("Token payload:", to_encode)  # Debugging: Print the token payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print("Encoded JWT:", encoded_jwt)  # Debugging: Print the encoded JWT
    return encoded_jwt
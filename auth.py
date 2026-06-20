from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Set tokenUrl to the login route so OpenAPI points to it
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

## token creation
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

## verify token - declare dependency on oauth2_scheme so FastAPI adds security scheme to OpenAPI
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


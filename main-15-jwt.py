"""
OAuth2 with Password (and hashing), Bearer with JWT tokens
"""
from datetime import timedelta, datetime
from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException, status, Security
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes
)
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()

# to get a string like this run >>$ openssl rand -hex 32
SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 5

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='token',
    scopes={'me': 'Read information about the current user.', 'items': 'Read items.'},
)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


class BaseUser(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None


class User(BaseUser):
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=5)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes:
        authenticate_value = f'Bearer scope={security_scopes.scope_str}'
    else:
        authenticate_value = f'Bearer'

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': authenticate_value},
    )

    permission_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Not enough permissions!',
        headers={'WWW-Authenticate': authenticate_value},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub', None)
        if username is None:
            raise credentials_exception
        token_scopes: List = payload.get('scopes', [])
        token_data = TokenData(username=username, scopes=token_scopes)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)

    if user is None:
        raise credentials_exception
    print(security_scopes.scopes)
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise permission_exception

    return user


async def get_current_active_user(current_user: User = Security(get_current_user, scopes=['me'])):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user


@app.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token(
        data={'sub': user.username, 'scopes': form_data.scopes},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/users/me', response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# @app.get('/users/me/items/')
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{'item_id': 'Foo', 'owner': current_user.username}]


@app.get('/users/me/items/')
async def read_own_items(
    current_user: User = Security(get_current_active_user, scopes=['items'])
):
    return [{'item_id': 'Foo', 'owner': current_user.username}]


@app.get('/status/')
async def read_system_status(current_user: User = Depends(get_current_user)):
    return {'status': 'ok'}



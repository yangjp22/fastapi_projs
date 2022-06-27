# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-22, Wed, 23:13
@Author: Jinpeng Yang
@Description: Security Tutorial
"""

from fastapi import Depends, FastAPI, HTTPException, status
from typing import Optional, Union
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext  # passlib 处理哈希加密的包
from datetime import timedelta, datetime


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI()

# 声明该URL是客户端应用于获取token的URL，该信息在OpenAPI中使用，然后在交互式API文档系统中使用
# 该oauth2_schema变量的一个实例，但它是一个"通知", 告知后台token体系已经工作了
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[str] = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded",
        email="fredyang@gmail.com",
        full_name="fred yang"
    )


async def get_current_user(token: str = Depends(oauth2_schema)):
    print("token: ", token)
    user = fake_decode_token(token)
    return user


@app.get("/users/me")   # 需要加入 Authorization: Bearer xxxx， 此中的xxx则会被当作token值
async def read_me(current_user: User = Depends(get_current_user)):  # Authorization: str =
    return current_user


@app.get('/items/')
async def read_items(token: str = Depends(oauth2_schema)):
    return {"token": token}


@app.get('/item/')
async def read():
    return {'msg': "hello world"}


# 用户数据 （模拟）
fake_users_db = {
    'johndoe': {
        "username": 'johndoe',
        'full_name': 'John Doe',
        'email': 'jhondoe@gmail.com',
        'hashed_pwd': 'fakehashedjohndoe',
        'disabled': False
    },
    'alice': {
        "username": 'alice',
        'full_name': 'Alice John',
        'email': 'alice@gmail.com',
        'hashed_pwd': 'fakehashedalice',
        'disabled': True
    }
}


# 哈希密码 （模拟）
def fake_hash_pwd(pwd: str):
    return "fakehashed" + pwd


# 用户输入模型
class UserInDB(User):
    hashed_pwd: str  # 哈希过后的密码


# 获取用户，返回User对象
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# 解码令牌（模拟）
# 此token为username
def fake_decode_token(token: str):
    user = get_user(fake_users_db, token)
    return user


# 获取当前用户
# 如果用户不存在或者处于非活跃状态，这这两个依赖项都将仅返回HTTP错误
# 此token为Authentication：Bearer xxxx 中的xxxx部分
# 从内容上来看是 username的
async def get_current_user(token: str = Depends(oauth2_schema)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


# 获取当前活跃用户，get （read_users_me) 专属
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


## 用户登陆，登陆成功后返回token给浏览器
## 此url就是/token， 和oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token")中tokenUrl的值要匹配一样
@app.post("/token")  # name = johndoe alice pwd = secret secret2
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.__dict__)
    # 此时的username是来自于前端提供的表单 name=username value="xxx"
    user_dict = fake_users_db.get(form_data.username)

    # 如果用户不存在
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # 用户存在，但密码不匹配
    # 先将这些数据放到Pydantic UserInDB模型中
    user = UserInDB(**user_dict)
    hashed_pwd = fake_hash_pwd(form_data.password)
    if not user.hashed_pwd == hashed_pwd:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # 如果成功登陆，则返回token信息给浏览器
    return {'access_token': user.username, 'toke_type': 'bearer'}


@app.get('/users/me')
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


fake_users_db_02 = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


# Context是上下文 CryptContext是密码上下文 schemes是计划 bcrypt是加密算法
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


# verify_password验证密码 plain_password为普通的密码 hashed_password哈希后的密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 获取哈希密码，即加密
def get_hashed_password(password):
    return pwd_context.hash(password)


# 验证用户
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    # 用户不存在或者密码验证不成功
    if not user or not verify_password(password, user.hashed_pwd):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}  # 验证不成功，需要在异常headers中有www-authenticate
        )
    return user   # <class '__main__.UserInDB'>


# 创建访问token, 中间添加了到期日期
def create_access_token(*, data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    # 对token进行加密，并返回加密后的token
    # 在用户进行登陆之后 会随着响应一起传回浏览器
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 获取当前用户 （需要在有token令牌的时候，可以省去登陆，直接拿到用户信息）
async def get_current_user_02(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 首先对从浏览器传来的token进行解密
        # payload: {token: {'access_token': xxx, 'token_type': xxx}, sub: username}
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # 根据token，获取相关的用户信息
    user = get_user(fake_users_db_02, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# 获取当前活跃用户 （前提是拿到当前用户）
async def get_current_active_user_02(current_user: User = Depends(get_current_user_02)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)  # 生成token令牌返回给浏览器
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. 验证用户，返回 <class '__main__.UserInDB'>
    user = authenticate_user(fake_users_db_02, form_data.username, form_data.password)
    # 2. access_token_expires访问令牌过期
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 3. create_access_token创建访问令牌 返回 <class '__main__.dict'>
    access_token = create_access_token(data={'sub': user.username},
                                       expires_delta=access_token_expires)
    # 返回
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/users2/me/', response_model=User)
async def read_users_me_02(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get('/users2/me/items/')
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{'item_id': "Foo", 'owner': current_user.username}]

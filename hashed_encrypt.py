# coding:utf8
import jwt
from passlib.context import CryptContext  # passlib 处理哈希加密的包


# Context 是上下文
# CryptContext 是密码上下文
# schemes 是计划
# bcrypt 是加密算法
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# verify_password验证密码 plain_password为普通的密码 hashed_password哈希后的密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 获取哈希密码，即加密
def get_hashed_password(password):
    return pwd_context.hash(password)


if __name__ == "__main__":

    # 验证哈希密码用法
    # 一个明文可以有多个哈希后的密文
    xxx = get_hashed_password('cccccc')
    yyy = get_hashed_password('cccccc')
    # print(xxx, yyy)
    # print(get_hashed_password('secret'))
    # print('verify_password: ', verify_password('cccccc', xxx))
    # print('verify_password: ', verify_password('cccccc', yyy))

import bcrypt


# 密码加密（bcrypt 会自动生成随机盐，不需要手动处理盐值）
def get_hash_password(password: str) -> str:
    # 明文转字节 -> hashpw 加密 -> 转回字符串存入数据库
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


# 校验密码（登录时用：用户输入的明文与数据库存的哈希比对）
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

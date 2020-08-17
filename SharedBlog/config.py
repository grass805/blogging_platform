# -*- coding: utf-8 -*
import os



#config
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:12345678@localhost/blogmysql'


# SECRET_KEY: flask及其相關extension需要加密，例如: flask的session， 其extension如  Flask-WTF的CSRF保护  Flask-Images  Cookies
# 考虑到安全性, 密钥不建议存储在程序中. 最好存储在系统环境变量中(另外寫一個.py檔), 通过 os.getenv(key, default=None) 获得
# app.secret_key='a_secret_key'   <-- 不好的寫法
# app.config['SECRET_KEY'] = os.urandom(24)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345678@localhost/blogmysql'
SECRET_KEY = os.urandom(24)


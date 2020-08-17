# -*- coding: utf-8 -*
'''
模塊初始化文件(必須)
資料夾名稱==模塊名稱
!!!注意順序!!!
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache




app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# cache.init_app(app, config={'CACHE_TYPE': 'simple'})
# cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

#werkzeug.contrib.cache從2014已被棄用
#基於werkzeug的flask_cache自2016改名為flask_caching

from .blueprint import blog  #from .資料夾 import blueprint物件名稱 資料夾前面要有.，不然是package名稱
# blog = Blueprint('blogs', __name__) <--不可行，@blog找不到url
app.register_blueprint(blog)


#執行程式
from . import main



# -*- coding: utf-8 -*-
from flask import Blueprint


blog = Blueprint('blogs', __name__)





'''
這個藍圖只能在此資料夾下的檔案被執行
'''

from . import entry
from . import blogs
from . import manage

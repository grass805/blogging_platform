# -*- coding: utf-8 -*
'''
跑這個檔案
!!!!与应用模块平级!!!!
'''
from SharedBlog import app


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run(host='0.0.0.0', port=80)
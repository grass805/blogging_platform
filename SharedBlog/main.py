# -*- coding: utf-8 -*
from flask import redirect, url_for, render_template, flash
from flask import session

from SharedBlog import app, db
from SharedBlog.db_model import t_user, t_cate, t_post





@app.route('/', methods=['GET']) #沒寫methods的話，預設是GET
def index():
    db.create_all()

    posts = db.session.query(t_post).all()  #這是一個list 同於 t_post.query.all()
    user_list = []
    for i in posts:
        user_id=i.user_id
        user=t_user.query.filter_by(id=user_id).first()
        user_list.append(user)
        
    print('user_list ', user_list)
    return render_template('index.html', posts=posts, user_list=user_list)

        
    


@app.route('/logout', methods=['GET'])
def logout():
    if 'user_key' in session :
        session.pop('user_key')
        flash('Logout Successful.')
    else:
        error1='You are not logged in.'
        error2='Sign up and Create your own Blog !'
        return render_template('error.html', error1=error1, error2=error2)
    
    return redirect(url_for('index'))










    
    
    
        
        
        
    




    
    
    
    
    


        


    
    
            
            
        




# -*- coding: utf-8 -*-
from flask import redirect, url_for, render_template, request
from flask import session, flash

from SharedBlog import db
from SharedBlog.db_model import t_user, t_cate, t_post
from SharedBlog import app
from . import blog

import bcrypt


'''
@blog可以繼承@app的函數，
並且必須放到.py (或定義__init__的資料夾)才能執行
但main.py中無法執行任何@blog的函數

'''


# @blog.context_processor
def parse_layout(user):
    print('execute to parse_layout')
    categories = t_cate.query.filter_by(user_id=user.id ).all()
    cate_post_n=[]
    for i in categories:
        cate_post= t_post.query.filter_by(cate_id=i.id).all()
        cate_post_n.append(len(cate_post))
    
    if 'user_key' in session : #如果已登入，則獲取登入者資料
        username = session['user_key']
        cur_user = t_user.query.filter_by(username=username).first()
        print('parse_layout: cur_user',cur_user)
    
    else: 
        cur_user = False   #代表沒登入
        print('parse_layout: cur_user',cur_user)
    
    blog_category = categories
    cate_post_n = cate_post_n
    current_user = cur_user
    print('parse_layout: user',user)

    return blog_category, cate_post_n, current_user


@app.template_global()  #可以給 屬於blog blueprint route 下的html使用的函數，記得要有()
def if_owner(user, current_user): #user是blog_owner，current_user是登入者
    print('execute to blog.if_owner')
    print('user:', user,'current_user:',current_user)
    if user==current_user:
        print('if_owner==TRUE')
        return True
    else:
        print('if_owner==FALSE')
        return False
    




@app.route('/login', methods=['GET', 'POST'])
def users_login():
    #local variable要先定義
    error = None
    #client端輸入的username和password經由request.form.get從html得到
    if request.method == 'POST' :
        stored_u = request.form.get('input_u')
        input_p = request.form.get('input_p')
        
        # first():返回查詢結果的第一個結果,如果未找查到,返回None
        # filter_by(欄位=x值): 篩選出是x值的欄位
        if t_user.query.filter_by(username=stored_u).first() == None: 
            error = 'User not found.'
        else:
            hashed_p = t_user.query.filter_by(username=stored_u).first().password
            #兩邊數據都要encode
            if bcrypt.checkpw(input_p.encode('utf8'), hashed_p.encode('utf-8')):
                #在session(字典)中增加user，並assign對應值
                #建立一個session用來對應已登入用戶，把用戶名稱username儲存進去
                session['user_key'] = stored_u
                flash('Login success !')
                
                user = t_user.query.filter_by(username=stored_u).first()
                
                return redirect(url_for('blogs.home', user_id=user.id))
            
            else:
                error = 'Password incorrect.'
        
    return render_template('login.html', error=error)



@app.route('/signup', methods=['GET', 'POST'])
def users_signup():
    error = None
    
    if request.method == 'POST' :
        create_u = request.form.get('create_u')
        create_p = request.form.get('create_p')
        
        if t_user.query.filter_by(username=create_u).first() :
            error = 'This username is already taken.'
        else:
            salt = bcrypt.gensalt()
            #TypeError("Unicode-objects must be encoded before hashing"
            hashed_p = bcrypt.hashpw(create_p.encode('utf8'), salt)
            add_user = t_user( username=create_u, password=hashed_p)
            db.session.add(add_user)
            db.session.commit()
            
            user_id = add_user.id
            #建立預設類別(uncategorized)
            default_cate = t_cate(user_id=user_id)
            db.session.add(default_cate)
            db.session.commit()
            
            flash('User created !')
            
            user = add_user
            session['user_key'] = user.username
            
            
            return redirect(url_for('blogs.home', user_id=user_id))
    
    return render_template('signup.html', error=error)


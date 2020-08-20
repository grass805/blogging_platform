# -*- coding: utf-8 -*-
from flask import redirect, url_for, render_template, request
from flask import session

from SharedBlog import db
from SharedBlog.db_model import t_user, t_cate, t_post
from . import blog
from .entry import parse_layout

from datetime import datetime

'''
blog頁面已有blog_owner(user)和current_user(login)的資訊
html中if_owner(user, current_user)確認是否為同一個user，True才會出現連結
但為了防止直接輸入url也可以編輯，
從登入session中得到登入者user資訊，以此來抓資料，
這樣也只能編輯自己的資料
'''
    
        
@blog.route('/about/edit', methods=['GET', 'POST']) #一個user只能有一個about，故沒有輸入user_id參數
def edit_about():
    if 'user_key' in session :
        cur_username = session['user_key'] #值是username
        cur_user = t_user.query.filter_by(username=cur_username).first()
        old_author=cur_user.author
        old_title=cur_user.blog_title
        old_about=cur_user.about
        
        blog_category, cate_post_n, current_user = parse_layout(cur_user) 
        
        if request.method == 'POST':
            set_title = request.form.get('set_title')
            edit_about = request.form.get('edit_about')
            edit_author = request.form.get('edit_author')
            
            
            if not edit_author :
                edit_author = old_author
            if not set_title :
                set_title = old_title
            if not edit_about:
                edit_about = old_about
            
            cur_user.blog_title = set_title
            cur_user.about = edit_about
            cur_user.author = edit_author
            db.session.commit()
            
            return redirect(url_for('blogs.about', user_id=cur_user.id))
        
    else:
        error1='You are not logged in.'
        error2='Sign up and Create your own Blog !'
        return render_template('error.html', error1=error1, error2=error2)
        
    return render_template('edit_about.html', old_author=old_author, old_title=old_title, old_about=old_about,
                           user=cur_user, blog_category=blog_category, cate_post_n=cate_post_n, current_user=current_user)



@blog.route('/add', methods=['GET', 'POST'])
def add_post():
    if 'user_key' in session :
        cur_username = session['user_key'] #值是username
        cur_user = t_user.query.filter_by(username=cur_username).first()
        
        blog_category, cate_post_n, current_user = parse_layout(cur_user)
        
            
        if request.method == 'POST':
            add_t = request.form.get('add_t')
            add_b = request.form.get('add_b')
            if not add_t or not add_b:
                return redirect(url_for('blogs.home', user_id=cur_user.id))
            #預設分類到這個使用者的uncategorized
            cate_id = t_cate.query.filter_by(user_id=cur_user.id, cate='uncategorized').first().id
            add_p = t_post(title=add_t, body=add_b, user_id=cur_user.id , cate_id=cate_id)
            db.session.add(add_p)
            db.session.commit()
            
            post_id = add_p.id
            return redirect(url_for('blogs.show_post', post_id=post_id))
    else:
        error1='You are not logged in.'
        error2='Sign up and Create your own Blog !'
        return render_template('error.html', error1=error1, error2=error2)
    
    return render_template('add_post.html',
                           user=cur_user, blog_category=blog_category, cate_post_n=cate_post_n, current_user=current_user)


'''
不用'POST'?
https://developer.huawei.com/consumer/cn/forum/topicview?tid=0201301473460400105&fid=23
'''
@blog.route('/manage', methods=['GET'])
def manage_post():
    if 'user_key' in session :
        cur_username = session['user_key'] #值是username
        cur_user = t_user.query.filter_by(username=cur_username).first()
        
        blog_category, cate_post_n, current_user = parse_layout(cur_user)
        
        data = t_post.query.filter_by(user_id=cur_user.id).all()  #這是一個list
        
        #創一個list，儲存 類別名稱
        #dict_cate = dict()
        #dictName[key] = value
        list_cate = []
        for i in data:
            cate_id = i.cate_id
            print('cate', i )
            print('cate id', cate_id)
            cate_name = t_cate.query.filter_by(id=cate_id).first().cate
            list_cate.append(cate_name)
            print(list_cate)
        
    else:
        error1='You are not logged in.'
        error2='Sign up and Create your own Blog !'
        return render_template('error.html', error1=error1, error2=error2)
    
    return render_template('manage.html', data_frompy=data, list_cate=list_cate,
                           user=cur_user, blog_category=blog_category, cate_post_n=cate_post_n, current_user=current_user)
        
#實現批量刪除按鈕功能，注意網址不會跳轉到/manage/delete
@blog.route('/manage/delete', methods=['GET'])
def delete_post():
    if 'user_key' in session :
        data_back = request.values.get("to_delete")  #傳來的值"to_delete"已转成json字符串
        print('data_back', data_back)
        data_list = eval(data_back) #通过eval方法将json格式转化成list
        print('data_list', data_list)
        for i in data_list:
            print("i", i)
            if t_post.query.filter_by(id=i).first() :
                selected_p = t_post.query.filter_by(id=i).first()
                db.session.delete(selected_p)
                db.session.commit()
        #return redirect(url_for(manage_post)) 結果不會跳轉頁面,因為那是前端(html)負責的!
    else:
        error1='You are not logged in.'
        error2='Sign up and Create your own Blog !'
        return render_template('error.html', error1=error1, error2=error2)
    
    return 'this message will not be shown'

#實現edit按鈕功能
@blog.route('/manage/edit', methods=['GET'])
def go_post():
    if 'user_key' in session :
        data_back = request.values.get("post_id")
        print('data_back', data_back)
        data_list = eval(data_back) 
        print('data_list', data_list)
        # redirect(url_for('show_post', post_id=data_list))
        edit_post(data_list)
    else:
        error1='You are not logged in.'
        error2='Sign up and Create your own Blog !'
        return render_template('error.html', error1=error1, error2=error2)
    
    return 'this message will not be shown'








#單純只能編輯文章，不能編輯或選擇類別
@blog.route('/manage/edit/<int:post_id>', methods=['GET', 'POST'])  #一個user可有多篇post，需要傳入post_id
def edit_post(post_id):
    post = t_post.query.filter_by(id=post_id).first()
    old_t = post.title
    old_b = post.body
    cate_id = post.cate_id
    cate_name = t_cate.query.filter_by(id=cate_id).first().cate
    
    user_id = post.user_id
    user = t_user.query.filter_by(id=user_id).first()
        
    if 'user_key' in session and session['user_key'] == user.username : #因為有了post_id，可以直接比對登入者和貼文作者是否為同一人
        cur_username = session['user_key'] #值是username
        cur_user = t_user.query.filter_by(username=cur_username).first()
        
        blog_category, cate_post_n, current_user = parse_layout(cur_user)  #仍然是套登入者的layout而非貼文作者
        
        if request.method == 'POST':
            edit_t = request.form.get('edit_t')
            edit_b = request.form.get('edit_b')
            time = datetime.now()
            
            if not edit_b :
                edit_b = old_b
            
            if not edit_t :
                edit_t = old_t
            
                
            post.title = edit_t
            post.body = edit_b
            post.timestamp = time
            db.session.commit()
            
            return redirect(url_for('blogs.show_post', post_id=post_id))
    
    else:
        error1='You are not logged in.'
        error2='Sign up and Create your own Blog !'
        return render_template('error.html', error1=error1, error2=error2)
    
        
    return render_template('edit_post.html', post_id=post_id, cate_name=cate_name, old_b=old_b, old_t=old_t,
                           user=cur_user, blog_category=blog_category, cate_post_n=cate_post_n, current_user=current_user)




@blog.route('/manage/cate/<int:post_id>', methods=['GET','POST'])
def manage_cate(post_id):
    if 'user_key' in session :
        cur_username = session['user_key'] #值是username
        cur_user = t_user.query.filter_by(username=cur_username).first()
        
        blog_category, cate_post_n, current_user = parse_layout(cur_user)
        #所有categories就是blog_category
        
    else:
        error1='You are not logged in.'
        error2='Sign up and Create your own Blog !'
        return render_template('error.html', error1=error1, error2=error2)
    
    return render_template('edit_cate.html', post_id=post_id,
                           user=cur_user, blog_category=blog_category, cate_post_n=cate_post_n, current_user=current_user)



#實現選擇cate按鈕
@blog.route('/manage/cate/select/<int:post_id>', methods=['GET','POST'])
def select_cate(post_id):
    if 'user_key' in session :
        cur_post = t_post.query.filter_by(id=post_id).first()
        
        data_back = request.values.get("cate_id") 
        print('data_back', data_back)
        data_list = eval(data_back) 
        print('data_list', data_list)
        
        # cate = t_cate.query.filter_by(id=data_list).first()
        # cate_id = cate.id
        cur_post.cate_id = data_list
        db.session.commit()
    
    else:
        error1='You are not logged in.'
        error2='Sign up and Create your own Blog !'
        return render_template('error.html', error1=error1, error2=error2)
    
    return 'this message will not be shown'

#實現刪除cate按鈕
@blog.route('/manage/cate/delete', methods=['GET'])
def delete_cate():
    if 'user_key' in session :
        cur_username = session['user_key'] #值是username
        cur_user = t_user.query.filter_by(username=cur_username).first()
        data_back = request.values.get("delete_cate") 
        print('data_back', data_back)
        data_list = eval(data_back) #通过eval方法将json格式转化成list
        print('data_list', data_list)
        
        cate = t_cate.query.filter_by(id=data_list).first()
        print('catename', cate.cate)
        cate_posts = t_post.query.filter_by(cate_id=cate.id).all()
        print('cate_posts', cate_posts)
        # if cate.cate == 'uncategorized' and cate_posts :  #list is not None永遠成立因為 空list是 []
        #     print('do nothing.')
        #     return 'do nothing.'
        # elif cate.cate == 'uncategorized' and not cate_posts :
        #     db.session.delete(cate)
        #     db.session.commit()
        if cate.cate == 'uncategorized':
            return 'do nothing.'
        else:
            if cate_posts :
                for i in cate_posts:
                    uncategorized = t_cate.query.filter_by(cate='uncategorized', user_id=cur_user.id).first()
                    i.cate_id = uncategorized.id
                    db.session.commit()
                db.session.delete(cate)
                db.session.commit()
            else:
                db.session.delete(cate)
                db.session.commit()  
    else:
        error1='You are not logged in.'
        error2='Sign up and Create your own Blog !'
        return render_template('error.html', error1=error1, error2=error2)
                
    return 'this message will not be shown'


#實現增加cate功能
@blog.route('/manage/cate/add', methods=['GET','POST'])
def add_cate():
    if 'user_key' in session :
        cur_username = session['user_key'] #值是username
        cur_user = t_user.query.filter_by(username=cur_username).first()
        
    
        if request.method == 'POST':
            new_cate = request.form.get('new_cate')
            if t_cate.query.filter_by(cate=new_cate, user_id=cur_user.id).first() :
                return redirect(url_for('blogs.manage_post'))
            else:
                cate = t_cate( cate=new_cate, user_id=cur_user .id)
                db.session.add(cate)
                db.session.commit()
        
    return redirect(url_for('blogs.manage_post'))
    
    





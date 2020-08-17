# -*- coding: utf-8 -*
from flask import render_template

from SharedBlog.db_model import t_user, t_cate, t_post

from . import blog
from .entry import parse_layout




@blog.route('/post/<int:post_id>', methods=['GET'])
def show_post(post_id):
    article = t_post.query.filter_by(id=post_id).first()
    cate_id = article.cate_id
    cate_name = t_cate.query.filter_by(id=cate_id).first().cate
    #要用.first()-- 用.get(參數)需要指定參數，用.all()不會出現資料
    
    user = t_user.query.filter_by(id=article.user_id).first()
    blog_category, cate_post_n, current_user = parse_layout(user)
    
    return render_template('post.html', article=article, post_id=post_id, cate_name=cate_name,
                           user=user, blog_category=blog_category, cate_post_n=cate_post_n, current_user=current_user)
                


@blog.route('/home/<int:user_id>', methods=['GET'])
def home(user_id):
    user = t_user.query.filter_by(id=user_id).first()
    posts = t_post.query.filter_by(user_id=user_id).all()  #這是一個list
    
    blog_category, cate_post_n, current_user = parse_layout(user)
    
    return render_template('home.html', posts=posts, 
                           user=user, blog_category=blog_category, cate_post_n=cate_post_n, current_user=current_user)


@blog.route('/about/<int:user_id>', methods=['GET'])
def about(user_id):
    user = t_user.query.filter_by(id=user_id).first()
    
    blog_category, cate_post_n, current_user = parse_layout(user)
    
    return render_template('about.html', 
                           user=user, blog_category=blog_category, cate_post_n=cate_post_n, current_user=current_user)


@blog.route('/category/<int:cate_id>', methods=['GET'])
def category(cate_id):
    cate = t_cate.query.filter_by(id=cate_id).first()
    cate_posts = t_post.query.filter_by(cate_id=cate_id).all()
    
    user = t_user.query.filter_by(id=cate.user_id).first()
    blog_category, cate_post_n, current_user = parse_layout(user)
    
    
    return render_template('show_cate.html', cate=cate, cate_posts=cate_posts,
                           user=user, blog_category=blog_category, cate_post_n=cate_post_n, current_user=current_user)




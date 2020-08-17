# -*- coding: utf-8 -*
from datetime import datetime
from SharedBlog import db
#from flask_sqlalchemy import SQLAlchemy 
#from main import db  傳入在main.py的db是可行的，但是main.py要傳入db_model的class是不可行的，-->要用模塊




class t_user(db.Model):
    __tablename__ = 'users'
    __table_args__ = {"mysql_charset" : "utf8"}  #否則只能輸入英文
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(20), nullable=False, unique=True, index=True)  #unique=True (設定為不重複值)
    password = db.Column(db.Text, nullable=False)  #bcrypt hash後最大72 byte
    blog_title = db.Column(db.String(100), nullable=True, index=True)
    author = db.Column(db.String(50), nullable=True)
    about = db.Column(db.Text, nullable=True)  # In general, TEXT objects do not have a length
    child_post = db.relationship('t_post', backref='users')
    child_cate = db.relationship('t_cate', backref='users')
    
    

class t_cate(db.Model):
    __tablename__ = 'category'
    __table_args__ = {"mysql_charset" : "utf8"}
    id = db.Column(db.Integer, primary_key=True)
    cate = db.Column(db.String(100), nullable=False, default='uncategorized')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    child_post = db.relationship('t_post', backref='category')
    
    
class t_post(db.Model):
    __tablename__ = 'posts'
    __table_args__ = {"mysql_charset" : "utf8"}
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(100), nullable=False, index=True) #index=True (建立索引值)，以供查詢
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    can_commit = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    cate_id = db.Column(db.Integer, db.ForeignKey('category.id',onupdate="CASCADE", ondelete="SET NULL") )
    
    
# class t_comment(db.Model):
    
    
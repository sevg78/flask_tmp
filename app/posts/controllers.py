from flask import (
    Blueprint,
    request,
    flash,
    redirect,
    url_for,
    render_template,
    render_template_string,
    jsonify,
)
import json
from datetime import datetime
from flask_login import current_user
from app.database import db
from app.models import Post, Tag


module = Blueprint('posts', __name__)


@module.route('/news')
def news():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('posts/news.html', posts=posts)

@module.route('/news/<slug>')
def news_detal(slug):
    post = Post.query.filter(Post.slug == slug).first()
    return render_template('posts/news_detail.html', post=post)

@module.route('/news/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    posts = tag.posts
    return render_template('posts/news_tag.html', posts=posts, tag=tag)
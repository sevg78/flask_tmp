from flask import (
    Blueprint,
    request,
    flash,
    redirect,
    url_for,
    render_template,
    render_template_string,
    jsonify,
    current_app,
)
import json
from datetime import datetime
from flask_login import current_user, login_required
from app.database import db
from app.models import Post, Tag, StatPost


module = Blueprint('posts', __name__)
app = current_app


@module.route('/news/')
def news():
    q = request.args.get('q')
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())
    pages = posts.paginate(page=page, per_page=app.config['PER_PAGE_NEWS'], error_out=False)
    return render_template('posts/news.html', posts=posts, pages=pages)


@module.route('/news/<slug>')
@login_required
def news_detal(slug):
    post = Post.query.filter(Post.slug == slug).first()
    post.count += 1
    stat = StatPost.query.filter(StatPost.user_id==current_user.id).all()
    st = [i.post_id for i in stat]
    if not(post.id in st):
        stat = StatPost(user_id=current_user.id, post_id=post.id)
        stat.count = 0
        stat.count += 1
        db.session.add(stat)
    else:
        stat = StatPost.query.filter(StatPost.user_id==current_user.id and StatPost.post_id==post.id).first()
        stat.count += 1
        db.session.add(stat)
    db.session.add(post)
    db.session.commit()
    return render_template('posts/news_detail.html', post=post)


@module.route('/news/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    posts = tag.posts
    return render_template('posts/news_tag.html', posts=posts, tag=tag)
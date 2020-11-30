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
import random
import os
from datetime import datetime
from flask_login import current_user, login_required
from app.database import db
from app.models import Post, Tag, StatPost, StorageImg
from app.posts.forms import CreatePostForm
from flask_ckeditor import upload_success, upload_fail

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


@module.route('/news/create_post')
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        print('=====>')
        return redirect(url_for(posts.news))
    return render_template('posts/create_post.html', create_post_form=form)


def allowed_file(filename):
    return not filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@module.route('/news/upload-image', methods=['POST'])
def upload_image_post():
    item = request.files.get('upload')
    if allowed_file(item.filename):
        return upload_fail(message="Допустимые типы загружаемых файлов: 'png', 'jpg', 'jpeg', 'gif'")
    hash = random.getrandbits(128)
    ext = item.filename.split('.')[-1]
    path = '{}.{}'.format(hash, ext)

    storage = StorageImg(
        name=item.filename,
        type=ext,
        path=path,
        user_id=current_user.id,
    )
    db.session.add(storage)
    db.session.commit()

    url = os.path.join(app.config['UPLOAD_FOLDER'], path)
    item.save(url)
    
    return upload_success(url=url)


@module.route('/news/check-file')
def check_file_handler():
    return render_template('file-browse.html', files=StorageImg.query.filter(StorageImg.user_id == current_user.id).all())

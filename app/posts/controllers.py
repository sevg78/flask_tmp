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
from app.models import Post


module = Blueprint('posts', __name__)


@module.route('/news')
def news():
    posts = Post.query.all()
    return render_template('posts/news.html', posts=posts)

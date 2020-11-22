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
from . . database import db

module = Blueprint('posts', __name__)



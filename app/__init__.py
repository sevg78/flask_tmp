import os
from flask import Flask, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_login import LoginManager, current_user
from flask_moment import Moment
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from app.database import db
from flask_ckeditor import CKEditor, CKEditorField


login_manager = LoginManager()
bootstrap = Bootstrap()
csrf_protect = CSRFProtect()
mail = Mail()
moment = Moment()
admin = Admin()
ckeditor = CKEditor()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    login_manager.init_app(app)
    login_manager.login_view = 'users.log'

    bootstrap.init_app(app)

    ckeditor.init_app(app)

    mail.init_app(app)

    csrf_protect.init_app(app)

    moment.init_app(app)

    import app.users.controllers as users
    app.register_blueprint(users.module)
    import app.posts.controllers as posts
    app.register_blueprint(posts.module)

    # Flask Admin

    from wtforms.fields import HiddenField
    from app.models import User, Role, Post, Tag, StorageImg

    class AdminMixin:
        def is_accessible(self):
            return current_user.is_administrator()

        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for('users.log', next=request.url))

    class BaseModelView(ModelView):
        def on_model_change(self, form, model, is_created):
            model.generate_slug()
            return super(BaseModelView, self).on_model_change(form, model, is_created)

    class HomeAdminView(AdminMixin, AdminIndexView):
        pass

    class AdminUserView(AdminMixin, ModelView):
        can_create = False
        column_exclude_list = ('password_hash')
        form_overrides = dict(password_hash=HiddenField)

    class RoleView(AdminMixin, ModelView):
        pass

    class ImgView(AdminMixin, ModelView):
        pass

    class PostView(AdminMixin, BaseModelView):
        column_exclude_list = ('slug')
        form_overrides = dict(slug=HiddenField, body=CKEditorField)
        create_template = 'admin/edit.html'
        edit_template = 'admin/edit.html'

    class TagView(AdminMixin, BaseModelView):
        column_exclude_list = ('slug')
        form_overrides = dict(slug=HiddenField)

    admin = Admin(app, 'Adminka', url='/', index_view=HomeAdminView(name='Home'), template_mode='bootstrap3')
    admin.add_view(AdminUserView(User, db.session))
    admin.add_view(RoleView(Role, db.session))
    admin.add_view(PostView(Post, db.session))
    admin.add_view(TagView(Tag, db.session))
    admin.add_view(ImgView(StorageImg, db.session))

    return app

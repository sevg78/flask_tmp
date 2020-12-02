from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[Length(0, 150), DataRequired('Это поле является обязательным.')])
    pre_body = TextAreaField('Пре-пост', validators=[DataRequired('Это поле является обязательным.')])
    body = CKEditorField('Пост', validators=[DataRequired('Это поле является обязательным.')])
    submit = SubmitField('Применить')

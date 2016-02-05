from wtforms import Form, StringField, TextAreaField, validators, SelectField

CATEGORIES = [("administration", "administration"), ("other", "other")]

class SearchForm(Form):
    tquery = StringField('query', validators=[validators.DataRequired(message=u'What are you searching ?'), validators.Length(min=3, message=u'Minimum 3 chars')])


class Form_New_Message(Form):
    title = StringField('title', validators=[validators.DataRequired(), validators.Length(max=100, message='max 100 characters')])
    author = StringField('author', validators=[validators.DataRequired(), validators.Length(max=20, message='max 20 characters')])
    category = SelectField('category', validators=[validators.DataRequired()], choices=CATEGORIES)
    message = TextAreaField('message', validators=[validators.DataRequired(), validators.Length(max=2048, message='max 2048 characters')])


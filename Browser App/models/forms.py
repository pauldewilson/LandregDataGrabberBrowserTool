from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class PostCodeForm(FlaskForm):

    postcode = StringField(label="Post Sector", render_kw={'placeholder': 'Input Post Sector (SE1 1AA -> SE1 1)'})
    submit = SubmitField(label='Go')
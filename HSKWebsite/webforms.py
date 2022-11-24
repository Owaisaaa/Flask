from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_wtf.file import FileField

# Create Teacher form
class TeacherForm(FlaskForm):
        tname = StringField("Teacher Name", validators=[DataRequired()], render_kw={"placeholder": " Enter Your Full Name "})
        sname   = StringField("Subject Name", validators=[DataRequired()], render_kw={"placeholder": " Enter Subject Name"})
        topictitle = StringField("Topic Title", validators=[DataRequired()], render_kw={"placeholder": " Enter Topic Title "})
        filename = FileField("Browse File", validators=[DataRequired()])
        submit = SubmitField("Submit")
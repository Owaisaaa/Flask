from flask import Flask, render_template, flash, request, send_file
from webforms import TeacherForm
from datetime import datetime
from io import BytesIO
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from werkzeug.utils import secure_filename

app=Flask(__name__)
app.config['SECRET_KEY'] = 'Passkey'
# New MySQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pwd123@localhost/StudyMaterial'

# Upload Folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)



# Create Model
class StudyMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacherName = db.Column(db.String(150), nullable=False)
    subNname = db.Column(db.String(200), nullable=False)
    topic = db.Column(db.String(300), nullable=False)
    #fileName = db.Column(db.String(300), nullable=False)
    fileData = db.Column(db.LargeBinary(length=(2**32)-1))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name


    # Create a route decorator
@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")

# Create Index Page
#@app.route("/index")
#def index():
#    return render_template("index.html")

# Create faculty Page
#@app.route("/faculty")
#def faculty():
#   return render_template("faculty.html")

# Create Teacher Page
@app.route("/teacher", methods=['GET', 'POST'])
def teacher():
    name = None     # name is a variable of this function
    form = TeacherForm()
    # Validator
    if form.validate_on_submit():
        teacher = StudyMaterial.query.filter_by(teacherName=form.tname.data).first()
        #file = request.files['filename']
        if teacher is None:
            teacher = StudyMaterial(teacherName=form.tname.data, subNname=form.sname.data,
                                    topic=form.topictitle.data, fileData=form.filename.data)     #fileData=file.read()
        db.session.add(teacher)
        db.session.commit()

        #This logic is used if file is uploaded to the folder but currently this is not working
        if (request.method == 'POST'):
            f = request.files['filename']
            f.save(os.path.join(app.config['UPLOAD_FOLDER']), secure_filename(f.filename))
        flash("Topic Uploaded Successfully!")
        name = form.tname.data
        form.tname.data = ''
        form.sname.data = ''
        #flash("Teacher Name already exists!")
    our_teachers = StudyMaterial.query.order_by(StudyMaterial.date_added)
    return render_template("teacher.html", form=form, name=name, our_teachers=our_teachers)

# Create Download Page
@app.route("/download")
def download():
    our_teachers = StudyMaterial.query.order_by(StudyMaterial.date_added)
    return render_template("download.html", our_teachers=our_teachers)

# Create route for file_download function
@app.route('/file_download/<int:id>')
def file_download(id):
    #file_id = StudyMaterial.query.get_or_404(id)
    our_teachers = StudyMaterial.query.order_by(StudyMaterial.date_added)
    file_id = StudyMaterial.query.filter_by(id=id).first()
    try:
        if file_id:
            #flash("File Downloaded")
            return send_file(BytesIO(file_id.data), attachment_filename=file_id.filename, as_attachment=True)
            flash("File Downloaded")
    except:
        return render_template("download.html", file_id=file_id, our_teachers=our_teachers)
        flash("Sorry there was a problem while downloading the file!!!")


# Delete a User from Database
@app.route('/file_delete/<int:id>')
def file_delete(id):
    user_to_delete = StudyMaterial.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!!!")
        our_users = StudyMaterial.query.order_by(StudyMaterial.date_added)

        return render_template("download.html", our_users=our_users)
    except:
        flash("Whoops! There was a problem while deleting the User, try again...")

        return render_template("download.html", our_users=our_users)


if __name__ == "__main__":
    app.run(debug=True)
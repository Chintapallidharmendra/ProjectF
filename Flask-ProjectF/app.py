import os
import sqlite3
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from loginForm import LoginForm ,updatePassword


info = [
{'name':'Dharmendra','roll':'U16EC058'},
{'name':'Siva Indraneel','roll':'U16EC068'},
{'name':'Kiran kumar','roll':'U16EC073'},
{'name':'Sudheer','roll':'U16EC075'},
]

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['UPLOAD_FOLDER'] = "C:/Users/Dharmendra/Desktop/ProjectF-Local/Flask-ProjectF/Data"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///credentials.db'
db = SQLAlchemy(app)

class LoginCredentials(db.Model):
  username = db.Column(db.String(2,20), primary_key=True, unique = True, nullable = False)
  pasword = db.Column(db.String(20), nullable = False)
  id = db.Column(db.Integer, nullable = False,unique = True)

@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/about")
def about():
	return render_template("about.html",info_dict =info,title = 'About')

@app.route("/books")
def books():
	return render_template("books.html",title = 'Books')

@app.route("/faculty")
def faculty():
	return render_template("faculty.html",title = 'Faculty')

@app.route("/get")
def get_bot_response():
     userText = request.args.get("msg") 
     return 'Sorry! Model not yet linked!'

@app.route("/getBooks")
def get_book_response():
     userBookText = request.args.get("bookInfo")
     return 'Sorry! Book Model not yet linked!'

@app.route("/getFaculty")
def get_faculty_response():
     userBookText = request.args.get("facultyInfo")
     return 'Sorry! Faculty Model not yet linked!'

@app.route("/login",methods = ['POST','GET'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    try:
      conn = sqlite3.connect('credentials.db')
      curs = conn.cursor()
      R_sql = "select * from LoginCredentials where id = 1;"
      curs.execute(R_sql)
      login_credentials = curs.fetchone()
      conn.commit()
      if form.username.data == login_credentials[0] and form.password.data == login_credentials[1]:
          flash('You have been logged in!', 'success')
          conn.close()
          return redirect(url_for('admin'))
      else:
        conn.close()
        flash('Login Unsuccessful. Please check username and password', 'danger')
    except:
      flash('Login Unsuccessful. Please check username and password')
  return render_template('login.html', title='Login', form=form)

@app.route("/admin",methods = ['POST','GET'])
def admin():
  updateform = updatePassword()
  if updateform.validate_on_submit():
    try:
      conn = sqlite3.connect('credentials.db')
      curs = conn.cursor()
      R_sql = "select * from LoginCredentials where id = 1;"
      curs.execute(R_sql)
      login_credentials = curs.fetchone()
      conn.commit()
      if updateform.username.data == login_credentials[0] and updateform.oldpassword.data == login_credentials[1]:
        U_sql = "update LoginCredentials set username='"+str(updateform.username.data)+"',password ='" + str(updateform.confirmpassword.data)+"' where id= 1;"
        curs.execute(U_sql)
        conn.commit()
        conn.close()
        flash("Password Reset succesful!!")
        return redirect(url_for('login'))
      else:
        conn.close()
        flash("Password Reset Unsuccesful !!")
        return redirect(url_for('home'))
    except:
      flash("Password Reset Unsuccesful !!")
      return redirect(url_for('home'))
  return render_template('adminPanel.html',title='AdminPanel',form=updateform)

@app.route('/success', methods = ['POST','GET'])  
def success():
  if request.method == 'POST':
    file = request.files['file']
    if file and file.filename in ['BookData.xlsx','FacultyData.xlsx']:
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      flash("uploaded succesfully !!")
      return redirect(url_for('admin'))
    else:
      flash("Upload Failed!!")
      return redirect(url_for('home'))
  else:
    flash("Update again!!")
    return redirect(url_for('admin'))


if __name__ == '__main__':
	app.run(debug = True)

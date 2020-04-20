from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
info = [
{'name':'Dharmendra','roll':'U16EC058'},
{'name':'Siva Indraneel','roll':'U16EC068'},
{'name':'Kiran kumar','roll':'U16EC073'},
{'name':'Sudheer','roll':'U16EC075'},
]
app = Flask(__name__)

@app.route("/")
@app.route("/chat")
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

if __name__ == '__main__':
	app.run(debug = True)

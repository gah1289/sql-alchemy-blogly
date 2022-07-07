"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User
from flask_sqlalchemy import SQLAlchemy
from seed import add_seed_data
# from flask_debugtoolbar import DebugToolbarExtension
# why do I always get an error?

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()
add_seed_data()

@app.route("/")
def show_users():

    users = User.query.all()
    return render_template("users.html", users = users)

@app.route("/add")
def show_add_user_form():
    '''Show form to add a user'''
    users = User.query.all()
    return render_template("add-user.html")

@app.route("/add", methods = ["POST"])
def add_user():
    '''Show form to add a user'''
    first_name=request.form['first-name']
    last_name = request.form['last-name']
    url = request.form['img-url']
    print(first_name)

    new_user = User(first_name=first_name, last_name=last_name, image_url = url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f"/details/{new_user.id}")

@app.route("/details/<user_id>")
def show_user_details(user_id):
    '''Show user detail page'''
    user = User.query.get_or_404(user_id)    
    return render_template("details.html", user=user)

@app.route("/details/<user_id>", methods=["POST"])
def user_action(user_id):
    '''Edit or delete'''
    user = User.query.get_or_404(user_id) 
    action= request.form['action'] 
    if action =='edit':
        return redirect(f"/edit/{user.id}")
    elif action == 'delete':
        User.query.filter(User.first_name == user.first_name, User.last_name == user.last_name).delete()
        db.session.commit();
        return render_template("deleted.html")
    elif action == 'home':
        return redirect("/")

@app.route("/edit/<user_id>")
def edit_user_form(user_id):
    '''Show edit user information form'''
    user = User.query.get_or_404(user_id) 
    return render_template("edit-user.html", user=user)

@app.route("/edit/<user_id>", methods = ["POST"])
def edit_user(user_id):
    '''Update user information'''
    user = User.query.get_or_404(user_id)
    user.first_name=request.form['first-name']
    user.last_name = request.form['last-name']
    user.url = request.form['img-url']    
    db.session.add(user)
    db.session.commit()
   
    return redirect("/")
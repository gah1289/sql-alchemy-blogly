"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag, PostTag
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
    tags=Tag.query.all()
    return render_template("home.html", users = users, tags=tags)

@app.route("/add-user")
def show_add_user_form():
    '''Show form to add a user'''
    users = User.query.all()
    return render_template("add-user.html")

@app.route("/add-user", methods = ["POST"])
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
    posts=Post.query.filter_by(user_id=user_id)    
    return render_template("details.html", user=user, posts=posts)

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

@app.route("/add-post/<user_id>")
def add_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags=Tag.query.all()
    return render_template('add-post.html', user=user, tags=tags)

@app.route("/add-post/<user_id>", methods=["POST"])
def add_post(user_id):
    post_title=request.form['post-title']
    post_content = request.form.get('post-content')
    tag_ids=[int(num) for num in request.form.getlist('tags')]
    tags=Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(user_id=user_id, post_title=post_title, post_content=post_content, tags=tags)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/details/{user_id}')

@app.route('/view-post/<user_id>-<post_id>')
def view_post(user_id, post_id):
    '''Take client to user post form'''
    post=Post.query.filter_by(user_id=user_id).filter_by(id=post_id).one()
    return render_template('/view-post.html', post=post)

@app.route('/view-post/<user_id>-<post_id>', methods=["POST", "GET"])
def post_action(user_id, post_id):
    '''Edit or delete'''
    post=Post.query.filter_by(user_id=user_id).filter_by(id=post_id).one()
    action= request.form.get('post-action')
    print(action)
    print(post.user_id)
    if action =='Cancel':
        return redirect(f'/details/{user_id}')
    elif action == 'Edit':
        return redirect(f"/edit-post/{user_id}-{post_id}")
    elif action == 'Delete':        
        Post.query.filter_by(user_id=user_id).filter_by(id=post_id).delete()
        db.session.commit();
        return render_template("deleted.html")

@app.route('/edit-post/<user_id>-<post_id>')
def edit_post_form(user_id, post_id):
    '''show edit post form'''
    post=Post.query.filter_by(user_id=user_id).filter_by(id=post_id).one()
    tags=Tag.query.all()
    return render_template('edit-post.html', post=post, tags=tags)

@app.route('/edit-post/<user_id>-<post_id>', methods=["POST"])
def edit_post(user_id, post_id):
    '''show edit post form'''
    post=Post.query.filter_by(user_id=user_id).filter_by(id=post_id).one()

    post.post_title=request.form.get('new-post-title')
    post.post_content = request.form.get('new-post-content')
    tag_ids=[int(num) for num in request.form.getlist('tags')]
    post.tags=Tag.query.filter(Tag.id.in_(tag_ids)).all()
    db.session.add(post)
    db.session.commit()
    return redirect(f'/details/{user_id}')

@app.route('/add-tag')
def show_add_tag_form():
    '''show list of tags'''
    tags=Tag.query.all()
    return render_template('add-tag.html', tags=tags)

@app.route('/add-tag', methods=["POST"])
def add_tag():
    '''add tag to tag list'''
    tag_name = request.form.get('tag-name')
    new_tag = Tag(name=tag_name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect(f'/')

@app.route('/show-tag/<tag_id>')
def show_tag(tag_id):
    '''show tag page'''
    tag=Tag.query.get(tag_id)
    return render_template('/show-tag.html', tag=tag)

@app.route('/edit-tag/<tag_id>')
def show_tag_edit_form(tag_id):
    '''show edit tag form'''
    tag=Tag.query.get(tag_id)
    return render_template('edit-tag.html', tag=tag)

@app.route('/edit-tag/<tag_id>', methods=["POST"])
def edit_tag(tag_id):
    '''show edit tag form'''
    tag=Tag.query.get(tag_id)
    tag.name=request.form.get('tag-name')
    db.session.add(tag)
    db.session.commit()
    return redirect(f'/show-tag/{tag_id}')

@app.route('/delete-tag/<tag_id>')
def delete_tag(tag_id):
    '''show edit tag form'''
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit();
    return render_template('deleted.html')
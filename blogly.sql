CREATE DATABASE blogly;
\c blogly;

db.drop_all();
db.create_all();
myspace_tom = User(first_name="Tom", last_name="Anderson", image_url = "/static/images/myspace-tom.jpg");
db.session.add(myspace_tom);
db.session.commit();
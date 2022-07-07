from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['TESTING']=True

db.drop_all()
db.create_all()

class UsersTestCase(TestCase):
    '''Test for users'''
    def setUp(self):
        '''Add a sample user'''
        User.query.delete()

        user = User(first_name="Tom", last_name="Anderson", image_url = "/static/images/myspace-tom.jpg");
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
    
    def tearDown(self):
        '''Clean up any failed tests'''
        db.session.rollback()
      
    def test_add_user_form(self):
        '''Test that Tom is added to list'''
        with app.test_client() as client:
            resp = client.get("/add")
            html= resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add User', html)
    
    def test_user_added(self):
        '''Test that Tom is added to list'''
        with app.test_client() as client:
            user=User(first_name="Gabby", last_name="McCarthy")
            db.session.add(user)
            db.session.commit()
            resp = client.get(f"/details/{user.id}")
            html= resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Gabby', html)
    def test_user_deleted(self):
        '''Test that user is deleted when you press delete button'''
        with app.test_client() as client:
            user=User(first_name="Gabby", last_name="McCarthy")
            db.session.add(user)
            db.session.commit()
            User.query.filter(User.first_name == user.first_name, User.last_name == user.last_name).delete()
            db.session.commit();
            resp = client.get(f"/details/{user.id}")

            self.assertEqual(resp.status_code, 404)

    def test_user_deleted(self):
        '''Test that user is deleted when you press delete button'''
        with app.test_client() as client:
            user=User(first_name="Gabby", last_name="McCarthy")
            db.session.add(user)
            db.session.commit()
            User.query.filter(User.first_name == user.first_name, User.last_name == user.last_name).delete()
            db.session.commit();
            resp = client.get(f"/details/{user.id}")

            self.assertEqual(resp.status_code, 404)

    
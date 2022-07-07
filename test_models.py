from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['TESTING']=True

db.drop_all()
db.create_all()

class UsersModelTestCase(TestCase):
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
      
    def test_show_user(self):
        '''Test that Tom is added to list'''
        with app.test_client() as client:
            resp = client.get("/")
            html= resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tom', html)
    
    
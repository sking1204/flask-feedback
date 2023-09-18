from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

#here we initilize bcrypt. The variable name we declare here should be used in our class method.
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)



class User(db.Model): 
    __tablename__ = 'users'    

    username = db.Column(db.String(20), 
                         nullable=False, 
                         unique=True,
                         primary_key=True)

    password = db.Column(db.Text, 
                         nullable=False)    
    email = db.Column(db.Text, 
                         nullable=False)    
    first_name = db.Column(db.Text, 
                         nullable=False)    
    last_name = db.Column(db.Text, 
                         nullable=False) 
    
    #research this
    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")
   

# start_register
    @classmethod
    def register(cls, username, pwd,email,first_name,last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name,last_name=last_name)
# end_register


# start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
# end_authenticate    

class Feedback(db.Model): 
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, 
                   primary_key=True)

    title = db.Column(db.String(100), 
                         nullable=False)

    content = db.Column(db.Text, 
                         nullable=False)    
    username = db.Column(db.Text, 
                         db.ForeignKey('users.username'),
                         nullable=False) 

    #a tweet can have one user, a user can have multiple tweets
    #here we are setting up a relationship betweent he user and tweets tables
    # #backref so we can go from user to tweets
    # user = db.relationship('User', backref="feedback")  
       
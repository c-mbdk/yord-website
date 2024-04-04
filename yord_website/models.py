from .extensions import db
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import Email, Length, DataRequired
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    """
    This class is for creating users, which can access the sensitive data on the website like the mailing list.

    Attributes
    ----------
    email : str
        the email address which will be the username
    password_hash: str
        the password transformed into a complicated string of characters using a password hashing algorithm
    authenticated: bool
        indicates whether the user has provided valid credentials or not
    """
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    authenticated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def is_active(self):
        """Default to True, as all users are active."""
        return True

    def get_id(self):
        """Return the user's email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    
    def set_password(self, password):
        """Creates a password hash for the password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verifies that the password provided by the user matches the hash."""
        return bcrypt.check_password_hash(self.password_hash, password)
    

class Member(db.Model):
    """
    This class is for creating members of the mailing list.

    Attributes
    ----------
    name : str
        forename and surname of the member
    email : str
        email address of the member
    date_added : date
        date that the member was added to the mailing list
    """

    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(320), nullable=False)
    email = db.Column(db.String(320), nullable=False, unique=True)
    date_added = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))

    def __init__(self, name, email):
        "Create a new Member object using their name, email address and the date they were added"
        self.name = name
        self.email = email
        self.date_added = datetime.now(timezone.utc)

    def __repr__(self):
        return f'Member {self.id}'
    

class LoginForm(FlaskForm):
    """
    This class is for creating the form used in the log in process.
    """
    username = StringField('Username', validators=[DataRequired()], render_kw={'placeholder': 'Username', 'class': 'input-login-item'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Password', 'class': 'input-login-item'})
    remember_me = BooleanField('Remember Me', render_kw={'class': 'checkbox'})
    submit = SubmitField('Log In', render_kw={'class': 'form-button'})


class RegistrationForm(FlaskForm):
    """
    This class is for creating the form used to join the mailing list.
    """
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100, message="Name must be between %(min)d and %(max)d characters.")], render_kw={'placeholder': 'Name', 'class': 'input'})
    email = StringField('Email', validators=[DataRequired(), Email(message="Please enter a valid email address."), Length(min=3, max=255, message="Email address must be between %(min)d and %(max)d characters.")], render_kw={'placeholder': 'Email address', 'class': 'input'})

class EditMemberDetailsForm(FlaskForm):
    """
    This class is for creating the form used to edit the individual members of the mailing list.
    """
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100, message="Name must be between %(min)d and %(max)d characters.")], render_kw={'class': 'edit-input'})
    email = StringField('Email', validators=[DataRequired(), Email(message="Please enter a valid email address."), Length(min=3, max=255, message="Email address must be between %(min)d and %(max)d characters.")], render_kw={'class': 'edit-input'})

class ContactForm(FlaskForm):
    """
    This class is for creating the contact form, used to send queries.
    """
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100, message="Name must be between %(min)d and %(max)d characters.")], render_kw={'placeholder': 'Name', 'class': 'contact-input'})
    email = StringField('Email', validators=[DataRequired(), Email(message="Please enter a valid email address.")], render_kw={'placeholder': 'Email address', 'class': 'contact-input'})
    query = TextAreaField('Query', validators=[DataRequired(), Length(min=5, max=300, message="Name must be between %(min)d and %(max)d characters.")], render_kw={'placeholder': 'Message', 'class': 'contact-input contact-query'})
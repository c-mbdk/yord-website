"""
This file (test_users.py) contains the unit tests for the User class in the models.py file.
"""
from yord_website.models import User

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN the User fields are defined correctly for the new user
    """

    first_user = User(email = 'test_usertest')
    first_user.set_password('check123!')
    first_user.authenticated = True

    assert first_user.email == 'test_usertest'
    assert first_user.password_hash != 'check123!'
    assert first_user.__repr__() == '<User test_usertest>'
    assert first_user.is_authenticated()
    assert not first_user.is_anonymous()

def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN the User fields are defined correctly for the new user
    """

    assert new_user.email == 'test_user'
    assert new_user.password_hash != 'test123$'
    assert new_user.__repr__() == '<User test_user>'
    assert new_user.is_authenticated()
    assert not new_user.is_anonymous()
    
def test_setting_password(new_user):
    """
    GIVEN an existing user
    WHEN a new password is set for the user
    THEN the new password is stored correctly and not as plaintext
    """   

    new_user.set_password('updatedPassword12£')

    assert new_user.password_hash != 'updatedPassword12£'
    assert new_user.password_hash != 'test123$'
    assert new_user.check_password('updatedPassword12£')
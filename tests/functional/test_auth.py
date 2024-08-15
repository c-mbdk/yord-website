"""
This file test_auth.py contains the functional tests for the 'auth' blueprint.

These tests check for the appropriate behaviour using POST and GET requests. 
"""

from flask import request

# Happy path
def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN the '200' status code is returned 
    """
    response = test_client.get('/login')
    html = response.data.decode("utf-8")

    assert "Log in" in html
    assert response.status_code == 200


def test_login_action(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to with valid credentials
    THEN the response is valid
    """
    response = test_client.post('/login',
                                data=dict(username='test_user', password='test123$'), follow_redirects=True)

    html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Manage mailing list" in html

def test_logout(test_client, init_database, log_in_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN the '/general' page is returned 
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/home"

def test_login_action_already_logged_in(test_client, init_database, log_in_default_user):
    """
    GIVEN a Flask application has been configured for testing and the user is already logged in
    WHEN the '/login' page is posted to
    THEN the user is redirected to the view the mailing list page
    """
    response = test_client.post('/login',
                                data=dict(username='test_user', password='test123$'), follow_redirects=True)
    html = response.data.decode("utf-8")  
    
    assert response.status_code == 200
    assert "Manage mailing list" in html
    assert not "Log in" in html
    assert response.request.path == '/members'

# Unhappy path
def test_invalid_login(test_client, init_database):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the '/login' page is posted to with invalid login details
    THEN 
    """
    response = test_client.post('/login',
                                data=dict(username='test_usercheck', password='test123$'), follow_redirects=True)
    html = response.data.decode("utf-8")
    
    assert "Unsuccessful login attempt. Please try again." in html
    assert not "Manage mailing list" in html
    assert response.request.path == '/login'


def test_missing_password_login(test_client_request):
    """
    GIVEN a Flask application has been configured for testing 
    WHEN the user tries to login without a password
    THEN the user is shown a validation error
    """

    with test_client_request.test_request_context("/login", method="POST", data={"username": "test_user", "password":""}):
        request.form["password"] == ['Please fill in this field.']

def test_missing_username_login(test_client_request):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the user tries to login without a username
    THEN the user is shown a validation error
    """

    with test_client_request.test_request_context("/login", method="POST", data={"username": "", "password":"test123$"}):
        request.form["username"] == ['Please fill in this field.']


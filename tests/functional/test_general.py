"""
This file (test_general.py) contains the functional tests for the 'general' blueprint. 

It uses a mixture of POST and GET requests to confirm the behaviour of multiple routes in the 'general' blueprint.
"""
from flask import request
from conftest import long_name, long_email

# Happy path
def test_home_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/home' page is requested (GET)
    THEN the '200' status code is returned
    AND an invitation to join the mailing list is present
    AND navigation links are present
    """
    response = test_client.get('/home')

    # make sure registration for mailing list text is present
    assert b"Join our mailing list" in response.data

    assert response.status_code == 200


def test_confirm_page(test_client):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the '/confirm' page is requested (GET)
    THEN the '200' status code is returned 
    """    

    response = test_client.get('/confirm', follow_redirects=True)
    html = response.data.decode("utf-8")
    
    assert "Thank you for subscribing" in html

    # haven't figured out how to track JavaScript redirects in pytest yet so this redirect will be tested more thoroughly via the UI-level tests
    assert "goToHomepage()" in html
    assert response.status_code == 200

def test_contact(test_client):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the '/contact' page is requested (GET)
    THEN the '200' status code is returned 
    """    

    response = test_client.get('/contact')
    html = response.data.decode("utf-8")

    assert "Contact us" in html
    assert "Got a query?" in html

    assert response.status_code == 200

def test_about(test_client):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the '/about' page is requested (GET)
    THEN the '200' status code is returned 
    """    

    response = test_client.get('/about')
    html = response.data.decode("utf-8")

    assert "What is YORD?" in html

    assert response.status_code == 200

def test_gallery(test_client):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the '/gallery' page is requested (GET)
    THEN the '200' status code is returned 
    """    

    response = test_client.get('/gallery')
    html = response.data.decode("utf-8")
    
    assert "PHOTO GALLERY" in html
    assert response.status_code == 200

def test_signup_error(test_client):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the '/error' page is requested (GET)
    THEN the '200' status code is returned 
    """    

    response = test_client.get('/error')

    assert b"Something went wrong while trying to add you to our mailing list" in response.data
    assert response.status_code == 200 

def test_signup_action_success(test_client, init_database):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the '/home' is successfully posted to with sign up data for the mailing list
    THEN the user is redirected to the 'general/confirm' page
    """
    data = {"name":'Polly Pocket', "email":'polly.pocket@gmails.com'}      
    response = test_client.post('/home', 
                                data=data, follow_redirects=True) 

    assert response.status_code == 200
    assert response.request.path == '/confirm'
    assert b"Thank you for subscribing" in response.data

# Unhappy path
def test_about_page_method_not_allowed(test_client):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the '/about' page is posted to (POST)
    THEN a '405' (Method Not Allowed) status code is returned 
    """        
    response = test_client.post('/about')
    assert response.status_code == 405

def test_gallery_page_method_not_allowed(test_client):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the '/gallery' page is posted to (POST)
    THEN a '405' (Method Not Allowed) status code is returned 
    """        
    response = test_client.post('/gallery')
    assert response.status_code == 405

def test_email_already_registered(test_client, init_database):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the '/home' is posted to with sign up data that already exists in the mailing list
    THEN the user is redirected to the 'general/home' page with an alert to inform them that the email address is already in use
    """
    data = {"name":'Polly Pocket', "email":'polly.pocket@gmails.com'}
    response = test_client.post('/home', 
                                data=data, follow_redirects=True) 

    assert response.status_code == 200
    assert response.request.path == '/confirm'

    response = test_client.post('/home', 
                                data=data, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == '/home'
    assert b"This email is already registered" in response.data                 

def test_register_missing_name(test_client_request, init_database):
    """
    GIVEN a Flask application has been configured for testing 
    WHEN the user tries to register for the mailing list without a name
    THEN the user is shown a validation error
    """ 
    with test_client_request.test_request_context("/home", method="POST", data={"name": "", "email":"lucy@gmails.com"}):
        request.form["name"] == ['Please fill in this field.']

def test_register_missing_email(test_client_request, init_database):
    """
    GIVEN a Flask application has been configured for testing 
    WHEN the user tries to register for the mailing list without an email address
    THEN the user is shown a validation error
    """ 
    with test_client_request.test_request_context("/home", method="POST", data={"name": "Lucy Doe", "email":""}):
        request.form["email"] == ['Please fill in this field.'] 

def test_register_name_less_than_min_length(test_client_request, init_database):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the user tries to register for the mailing list
    AND inputs a name shorter than the minimum length
    THEN the user is shown a validation error
    """              
    with test_client_request.test_request_context("/home", method="POST", data={"name": "", "email":"janey.doey@gmails.com"}):
        request.form["name"] == ['Name must be between 1 and 100 characters.']

def test_register_name_exceeds_max_length(test_client_request, init_database):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the user tries to register for the mailing list
    AND inputs a name greater than the maximum length
    THEN the user is shown a validation error
    """              
    with test_client_request.test_request_context("/home", method="POST", data={"name": long_name, "email":"janey.doey@gmails.com"}):
        request.form["name"] == ['Name must be between 1 and 100 characters.']

def test_register_email_less_than_min_length(test_client_request, init_database):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the user tries to register for the mailing list
    AND inputs an email address shorter than the minimum length
    THEN the user is shown a validation error
    """              
    with test_client_request.test_request_context("/home", method="POST", data={"name": "Janey Doe", "email":"j@"}):
        request.form["name"] == ['Email must be between 3 and 255 characters.']

def test_register_email_exceeds_max_length(test_client_request, init_database):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the user tries to register for the mailing list
    AND inputs an email address longer than the maximum length
    THEN the user is shown a validation error
    """              
    with test_client_request.test_request_context("/home", method="POST", data={"name": "Janey Doe", "email": long_email}):
        request.form["name"] == ['Email must be between 3 and 255 characters.']

def test_register_improper_email(test_client_request, init_database, log_in_default_user):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the user tries to register for the mailing list
    AND inputs an improperly formatted email
    THEN the user is shown a validation error
    """
    with test_client_request.test_request_context("/home", method="POST", data={"name": "Pat Butcher", "email":"pat.butcher.gmails.com"}):
        request.form["email"] == ['Please enter a valid email address.']                

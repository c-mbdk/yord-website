"""
This file (test_mailing.py) contains the functional tests for the 'mailing' blueprint. 

It uses a mixture of POST and GET requests to confirm the behaviour of multiple routes in the 'mailing' blueprint.
"""

from flask import request
from conftest import long_name, long_email

# Happy path
def test_view_members(test_client, init_database, log_in_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/mailing/members' page is requested (GET)
    THEN the 'Manage mailing list' page is displayed to the user
    """
    response = test_client.get('/mailing/members', follow_redirects=True)
    assert response.status_code == 200
    assert b"Manage mailing list" in response.data

def test_view_edit(test_client, init_database, log_in_default_user):
    """
    GIVEN a Flask application has been configured for testing and the user is logged in
    WHEN the '/mailing/edit/1' page is requested (GET)
    THEN the user is directed to a page to edit the member's details
    """
    response = test_client.get('/mailing/edit/1', follow_redirects=True)
    assert response.status_code == 200
    assert b"Edit member details" in response.data

def test_edit_action_successful(test_client, init_database, log_in_default_user):
    """
    GIVEN a Flask application has been configured for testing and the user is logged in
    WHEN the '/mailing/edit/1' page is posted to (POST) with data for an existing member
    THEN the user is directed to the 'Manage mailing list'
    """
    data = dict(name='Janey Doey', email='janey.doey@gmails.com')
    response = test_client.post('mailing/edit/1', data=data, follow_redirects=True) 

    assert response.status_code == 200
    assert response.request.path == '/mailing/members'
    assert b"Manage mailing list" in response.data

def test_delete_action_successful(test_client, init_database, log_in_default_user):
    """
    GIVEN a Flask application has been configured for testing and the user is logged in
    WHEN the '/mailing/delete/1' page is requested (GET)
    THEN the user is directed to the 'Manage mailing list'
    """
    response = test_client.get('/mailing/delete/1')

    assert response.status_code == 302
    assert b"/mailing/members" in response.data        

# Unhappy path
def test_delete_member_method_not_allowed(test_client, init_database, log_in_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/mailing/delete/1' page is posted to (POST)
    THEN the '405' (Method Not Allowed) status code is returned 
    """
    response = test_client.post('/mailing/delete/1', follow_redirects=True)
    assert response.status_code == 405

def test_view_all_not_logged_in(test_client):
    """
    GIVEN a Flask application is configured for testing
    WHEN the '/mailing/members' page is requested (GET) by an anonymous user
    THEN an error message is displayed
    """ 
    response = test_client.get('/mailing/members', follow_redirects=True)

    assert response.status_code == 200
    assert b"Manage mailing list" not in response.data

def test_edit_not_logged_in(test_client):
    """
    GIVEN a Flask application is configured for testing
    WHEN the '/mailing/edit/1' page is requested (GET) by an anonymous user
    THEN an error message is displayed
    """    
    response = test_client.get('/mailing/edit/1', follow_redirects=True)

    assert response.status_code == 200
    assert b"Edit member details" not in response.data

def test_edit_invalid_member(test_client, init_database, log_in_default_user):
    """
    GIVEN a Flask application is configured for testing
    WHEN the '/mailing/edit/456' page is requested (GET) by the user
    AND there is no member with an id=456
    THEN an error message is displayed
    """
    response = test_client.get('/mailing/edit/456', follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == '/mailing/members'

def delete_member_invalid_member(test_client, init_database, log_in_default_user):
    """
    GIVEN a Flask application is configured for testing
    WHEN the '/mailing/delete/233' page is requested (GET) by the user
    AND there is no member with an id=233
    THEN an error message is displayed
    """
    response = test_client.get('/mailing/delete/233', follow_redirects=True)

    assert response.status_code == 200
    assert b"There was an issue deleting the member from the mailing list." in response.data

def test_edit_member_missing_name(test_client_request, init_database, log_in_default_user):
    """
    GIVEN a Flask application has been configured for testing 
    WHEN the user tries to edit an existing member of the mailing list
    AND clears the name field
    THEN the user is shown a validation error
    """  
    with test_client_request.test_request_context("/mailing/edit/1", method="POST", data={"name": "", "email":"pat@eastenders.co.uk"}):
        request.form["name"] == ['Please fill in this field.']  

def test_edit_member_missing_email(test_client_request, init_database, log_in_default_user):
    """
    GIVEN a Flask application has been configured for testing 
    WHEN the user tries to edit an existing member of the mailing list
    AND clears the email field
    THEN the user is shown a validation error
    """  
    with test_client_request.test_request_context("/mailing/edit/1", method="POST", data={"name": "Pat Butcher", "email":""}):
        request.form["name"] == ['Please fill in this field.']

def test_edit_improper_email_format(test_client_request, init_database, log_in_default_user):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the user tries to edit an existing member of the mailing list
    AND inputs an improperly formatted email
    THEN the user is shown a validation error
    """
    with test_client_request.test_request_context("/mailing/edit/1", method="POST", data={"name": "Pat Butcher", "email":"pat.butcher.gmails.com"}):
        request.form["email"] == ['Please enter a valid email address']
 

def test_edit_name_less_than_min_length(test_client_request, init_database, log_in_default_user):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the user tries to edit an existing member of the mailing list
    AND inputs a name shorter than the minimum length
    THEN the user is shown a validation error
    """           
    with test_client_request.test_request_context("/mailing/edit/1", method="POST", data={"name": "", "email":"janey.doey@gmails.com"}):
        request.form["name"] == ['Name must be between 1 and 100 characters.']

def test_edit_name_exceeds_max_length(test_client_request, init_database, log_in_default_user):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the user tries to edit an existing member of the mailing list
    AND inputs a name longer than the maximum length
    THEN the user is shown a validation error
    """           
    with test_client_request.test_request_context("/mailing/edit/1", method="POST", data={"name": long_name, "email":"janey.doey@gmails.com"}):
        request.form["name"] == ['Name must be between 1 and 100 characters.']

def test_edit_email_less_than_min_length(test_client_request, init_database, log_in_default_user):
        """
        GIVEN a Flask application has been configured for testing
        WHEN the user tries to edit an existing member of the mailing list
        AND inputs an email address shorter than the minimum length
        THEN the user is shown a validation error
        """    
        with test_client_request.test_request_context("/mailing/edit/1", method="POST", data={"name": "Jane Doey", "email":"j@"}):
            request.form["email"] == ['Email address must be between 3 and 255 characters.']

def test_edit_email_exceeds_max_length(test_client_request, init_database, log_in_default_user):
        """
        GIVEN a Flask application has been configured for testing
        WHEN the user tries to edit an existing member of the mailing list
        AND inputs an email address longer than the maximum length
        THEN the user is shown a validation error
        """    
        with test_client_request.test_request_context("/mailing/edit/1", method="POST", data={"name": "Jane Doey", "email": long_email}):
            request.form["email"] == ['Email address must be between 3 and 255 characters.']
            
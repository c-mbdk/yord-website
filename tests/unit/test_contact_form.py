"""
This file (test_contact_form.py) contains the unit tests for the ContactForm class in the models.py file.
"""
from yord_website.models import ContactForm
from conftest import long_name, long_email, long_query

def test_contact_success(test_client):
    """
    GIVEN a ContactForm model
    WHEN a new ContactForm instance is created
    AND the fields have valid inputs
    AND the form is submitted
    THEN the form data will pass validation
    """
    form = ContactForm(
        name='Jane Doe',
        email='jane.doe@gmails.com',
        query='Hi I like ice cream'
        )
    
    assert form.validate() == True

def test_contact_fail_short_name(test_client):
    """
    GIVEN a ContactForm model
    WHEN a new ContactForm instance is created
    AND the name field has a shorter input than the permitted minimum length
    AND the form is submitted
    THEN the form data will fail validation
    """
    form = ContactForm(
        name='',
        email='jane.doe@gmails.com',
        query='I am a nobody'
    )
    assert form.validate() == False  

def test_contact_fail_long_name(test_client):
    """
    GIVEN a ContactForm model
    WHEN a new ContactForm instance is created
    AND the name field has a longer input than the permitted maximum length
    AND the form is submitted
    THEN the form data will fail validation
    """     
    form = ContactForm(
        name=long_name,
        email='janey.doe@gmails.com',
        query='here I am!'
    )

    assert form.validate() == False

def test_contact_fail_short_email(test_client):
    """
    GIVEN a ContactForm model
    WHEN a new ContactForm instance is created
    AND the email field has a shorter input than the permitted minimum length
    AND the form is submitted
    THEN the form data will fail validation
    """
    form = ContactForm(
        name='Jane Doe',
        email='j@',
        query='hiya hun'
    )
    assert form.validate() == False

def test_contact_fail_long_email(test_client):
    """
    GIVEN a ContactForm model
    WHEN a new ContactForm instance is created
    AND the email field has a longer input than the permitted maximum length
    AND the form is submitted
    THEN the form data will fail validation
    """
    form = ContactForm(
        name='Jane Doe',
        email=long_email,
        query='I like to sing in the bath'
    )
    assert form.validate() == False

def test_contact_fail_missing_email(test_client):
    """
    GIVEN a ContactForm model
    WHEN a new ContactForm instance is created
    AND the email field has no input
    AND the form is submitted
    THEN the form data will fail validation
    """
    form = ContactForm(
        name='Jane Doe',
        email='',
        query='bye bye'
    )
    assert form.validate() == False  

def test_contact_fail_invalid_email(test_client):
    """
    GIVEN a ContactForm model
    WHEN a new ContactForm instance is created
    AND the email field does not contain a valid input
    AND the form is submitted
    THEN the form data will fail validation
    """      
    form = ContactForm(
        name='Jane Doe',
        email='jane.doe.gmails.com',
        query='shhh please'
    )

    assert form.validate() == False

def test_contact_fail_long_query(test_client):
    """
    GIVEN a ContactForm model
    WHEN a new ContactForm instance is created
    AND the query field has a longer input than the permitted maximum length
    AND the form is submitted
    THEN the form data will fail validation
    """     
    form = ContactForm(
        name='Janey Doe',
        email='janey.doe@gmails.com',
        query=long_query
    )

    assert form.validate() == False

def test_contact_fail_short_query(test_client):
    """
    GIVEN a ContactForm model
    WHEN a new ContactForm instance is created
    AND the query field has a shorter input than the permitted minimum length
    AND the form is submitted
    THEN the form data will fail validation
    """
    form = ContactForm(
        name='Jane Doe',
        email='jane.doe@gmails.com',
        query='gghh'
    )
    assert form.validate() == False


"""
This file (test_registration_form.py) contains the unit tests for the RegistrationForm class in the models.py file.
"""
from yord_website.models import RegistrationForm
from conftest import long_name, long_email

def test_registration_success(test_client):
    """
    GIVEN a RegistrationForm model
    WHEN a new RegistrationForm instance is created
    AND the fields have valid inputs
    AND the form is submitted
    THEN the form data will pass validation
    """
    form = RegistrationForm(
        name='Jane Doe',
        email='jane.doe@gmails.com'
        )
    
    assert form.validate() == True

def test_registration_fail_short_name(test_client):
    """
    GIVEN a RegistrationForm model
    WHEN a new RegistrationForm instance is created
    AND the name field has a shorter input than the permitted minimum length
    AND the form is submitted
    THEN the form data will fail validation
    """
    form = RegistrationForm(
        name='',
        email='jane.doe@gmails.com'
    )
    assert form.validate() == False  

def test_registration_fail_long_name(test_client):
    """
    GIVEN a RegistrationForm model
    WHEN a new RegistrationForm instance is created
    AND the name field has a longer input than the permitted maximum length
    AND the form is submitted
    THEN the form data will fail validation
    """     
    form = RegistrationForm(
        name=long_name,
        email='janey.doe@gmails.com'
    )

    assert form.validate() == False

def test_registration_fail_short_email(test_client):
    """
    GIVEN a RegistrationForm model
    WHEN a new RegistrationForm instance is created
    AND the email field has a shorter input than the permitted minimum length
    AND the form is submitted
    THEN the form data will fail validation
    """
    form = RegistrationForm(
        name='Jane Doe',
        email='j@'
    )
    assert form.validate() == False

def test_registration_fail_long_email(test_client):
    """
    GIVEN a RegistrationForm model
    WHEN a new RegistrationForm instance is created
    AND the email field has a longer input than the permitted maximum length
    AND the form is submitted
    THEN the form data will fail validation
    """
    form = RegistrationForm(
        name='Jane Doe',
        email=long_email
    )
    assert form.validate() == False

def test_registration_fail_missing_email(test_client):
    """
    GIVEN a RegistrationForm model
    WHEN a new RegistrationForm instance is created
    AND the email field has no input
    AND the form is submitted
    THEN the form data will fail validation
    """
    form = RegistrationForm(
        name='Jane Doe',
        email=''
    )
    assert form.validate() == False  

def test_registration_fail_invalid_email(test_client):
    """
    GIVEN a RegistrationForm model
    WHEN a new RegistrationForm instance is created
    AND the email field does not contain a valid input
    AND the form is submitted
    THEN the form data will fail validation
    """      
    form = RegistrationForm(
        name='Jane Doe',
        email='jane.doe.gmails.com'
    )

    assert form.validate() == False
"""
This file (test_edit_member_form.py) contains the unit tests for the EditMemberDetailsForm class in the models.py file.
"""
from yord_website.models import EditMemberDetailsForm
from conftest import long_name, long_email

def test_edit_success(test_client, init_database):
    """
    GIVEN an EditMemberDetailsForm model
    WHEN a new EditMemberDetailsForm instance is created
    WHEN the fields have valid inputs
    AND the form is submitted
    THEN the form data will pass validation
    """
    form = EditMemberDetailsForm(
        name='Janey Doe',
        email='janey.doey@gmails.com'
    )

    assert form.validate() == True

def test_edit_fail_short_name(test_client, init_database):
    """
    GIVEN an EditMemberDetailsForm model
    WHEN a new EditMemberDetailsForm instance is created
    WHEN the name field has a shorter input than the permitted minimum length
    AND the form is submitted
    THEN the form data will fail validation
    """   
    form = EditMemberDetailsForm(
        name='',
        email='janey.doe@gmails.com'
    )

    assert form.validate() == False

def test_edit_fail_long_name(test_client, init_database):
    """
    GIVEN an EditMemberDetailsForm model
    WHEN a new EditMemberDetailsForm instance is created
    WHEN the name field has a longer input than the permitted maximum length
    AND the form is submitted
    THEN the form data will fail validation
    """     
    form = EditMemberDetailsForm(
        name=long_name,
        email='janey.doe@gmails.com'
    )

    assert form.validate() == False

def test_edit_fail_short_email(test_client, init_database):
    """
    GIVEN an EditMemberDetailsForm model
    WHEN a new EditMemberDetailsForm instance is created
    WHEN the email field has a shorter input than the permitted minimum length
    AND the form is submitted
    THEN the form data will fail validation
    """    
    form = EditMemberDetailsForm(
        name='Janey Doey',
        email='j@'
    )

    assert form.validate() == False

def test_edit_fail_long_email(test_client):
    """
    GIVEN an EditMemberDetailsForm model
    WHEN a new EditMemberDetailsForm instance is created
    WHEN the email field has a longer input than the permitted maximum length
    AND the form is submitted
    THEN the form data will fail validation
    """
    form = EditMemberDetailsForm(
        name='Janey Doey',
        email=long_email
    )

    assert form.validate() == False

def test_edit_fail_email_missing(test_client, init_database):
    """
    GIVEN an EditMemberDetailsForm model
    WHEN a new EditMemberDetailsForm instance is created
    WHEN the email field has no input
    AND the form is submitted
    THEN the form data will fail validation
    """    
    form = EditMemberDetailsForm(
            name='Janey Doey',
            email=''
        )

    assert form.validate() == False

def test_edit_fail_invalid_email(test_client, init_database):
    """
    GIVEN an EditMemberDetailsForm model
    WHEN a new EditMemberDetailsForm instance is created
    WHEN the email field does not contain a valid input
    AND the form is submitted
    THEN the form data will fail validation
    """
    form = EditMemberDetailsForm(
            name='Janey Doey',
            email='janey.doey.gmails.com'
        )

    assert form.validate() == False 
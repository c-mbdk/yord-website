from yord_website.models import Member

"""
This file (test_members.py) contains the unit tests for the Member class in the models.py file.
"""
def test_new_member(new_member):
    """
    GIVEN a Member model
    WHEN a new Member is created
    THEN the name and email fields are defined correctly for the new member
    """
    
    assert new_member.name == 'Jane Doey'
    assert new_member.email == 'jane.doe@gmails.com'

def test_update_member(new_member):
    """
    GIVEN an existing member
    WHEN the attributes of the member are updated
    THEN the member will retain the newly updated attributes
    """    
    
    new_member.name = 'Juliet Capulet'
    new_member.email = 'juliet.capulet@gmails.com'
    
    assert new_member.name == 'Juliet Capulet'
    assert not new_member.name == 'Jane Doe'

    assert new_member.email == 'juliet.capulet@gmails.com'
    assert not new_member.email == 'jane.doe@gmails.com'
"""
This file (test_database.py) contains the unit tests for the database transactions required for the YORD website app.
"""

from yord_website.models import Member, User
from yord_website import db
from sqlalchemy.exc import NoResultFound, InvalidRequestError
import pytest

# -----------------
# Testing core CRUD functions
# -----------------

def test_create_and_read_member(test_client, init_empty_database):
    """
    GIVEN a database has been initialised with a Member table
    WHEN a new member is created and read from the database
    THEN the member is successfully retrieved from the database
    """
    member = Member(
        name='Jane Doe', 
        email='jane.doe@gmails.com'
        )
    db.session.add(member)
    db.session.commit()
    new_member = db.session.execute(db.select(Member).filter_by(email="jane.doe@gmails.com")).scalar_one()
    assert new_member.name == 'Jane Doe'
    assert new_member.email == 'jane.doe@gmails.com'

def test_read_all_members(test_client, init_empty_database):
    """
    GIVEN a database has been initialised with a Member table
    WHEN the member entries are queried
    THEN all members are successfully retrieved from the database
    """   

    member = Member(
        name='Jools Doe', 
        email='jools.doe@gmails.com'
    )

    member_two = Member(
        name='Fikile Bhele', 
        email='fikile.bhele@gmails.com'
    )
    db.session.add_all([member, member_two])
    db.session.commit()

    members_results = db.session.execute(db.select(Member.name).order_by(Member.name)).all()
    members = [entry for entry in members_results]
    assert len(members) == 2
    assert 'Fikile Bhele' in members[0]
    assert 'Jools Doe' in members[1]

def test_read_all_members_db_empty(init_empty_database):
    """
    GIVEN a database has been initialised with a Member table
    WHEN the Member table is empty
    AND the Member table is queried
    THEN no records are returned
    """    
    members_results = db.session.execute(db.select(Member.name).order_by(Member.name)).all()
    members = [entry for entry in members_results]
    assert len(members) == 0

def test_update_member(init_empty_database):
    """
    GIVEN a database has been initialised with a Member table
    WHEN an existing member is updated
    THEN the updates are made to the member record in the database 
    """
    # Create initial record
    member = Member(
        name='Jeremy Doe',
        email='jeremy.doe@gmails.com'
    )
    db.session.add(member)
    db.session.commit()

    new_member = db.session.execute(db.select(Member).filter_by(email="jeremy.doe@gmails.com")).scalar_one()

    # Updating record
    new_member.email = 'jeramey.lb.doe@gmails.com'
    db.session.commit()

    updated_member = db.session.execute(db.select(Member).filter_by(email="jeramey.lb.doe@gmails.com")).scalar_one()

    assert updated_member.name == 'Jeremy Doe'
    assert updated_member.email == 'jeramey.lb.doe@gmails.com'

def delete_member(init_empty_database):
    """
    GIVEN a database has been initialised with a Member table
    WHEN a record is deleted from the Member table
    AND the database is queried for that member
    THEN the Member record cannot be retrieved from the database
    """  
    # Create initial record
    member = Member(
        name='Juliet Doe',
        email='juliet.doe@gmails.com'
    )
    db.session.add(member)
    db.session.commit()

    new_member = db.session.execute(db.select(Member).filter_by(email="juliet.doe@gmails.com")).scalar_one()

    assert new_member.name == 'Juliet Doe'

    # Actual delete
    db.session.delete(new_member)
    db.session.commit()

    # Assert delete is successful
    member_post_delete = db.session.execute(db.select(Member.email).order_by(Member.email)).all()
    remaining_members = [member for member in member_post_delete]

    assert not 'juliet.doe@gmails.com' in remaining_members

def test_delete_all_members(init_empty_database):
    """
    GIVEN a database has been initialised with a Member table
    WHEN all the entries in the Members table are deleted
    THEN no Member records can be retrieved from the table
    """ 
    member_one = Member(
        name='Julian Doe', 
        email='julian.doe@gmails.com'
    )

    member_two = Member(
        name='Puleng Khumalo', 
        email='puleng.khumalo@gmails.com'
    )
    db.session.add_all([member_one, member_two])
    db.session.commit()

    members_results = db.session.execute(db.select(Member.name).order_by(Member.name)).all()
    members = [entry for entry in members_results]
    assert len(members) == 2

    members_for_delete = db.session.execute(db.select(Member).order_by(Member.name)).scalars()
    for member in members_for_delete:
        db.session.delete(member)
        db.session.commit()

    members_post_delete = db.session.execute(db.select(Member).order_by(Member.name)).all()
    members_list = [entry for entry in members_post_delete]
    assert len(members_list) == 0
    

def test_create_and_read_user(init_empty_database):
    """
    GIVEN a database has been initialised with a User table
    WHEN a new user is created
    AND the database is queried
    THEN the new user is successfully retrieved
    """
    user = User(
        email='testing_user',
    )
    user.set_password('test123%')
    user.authenticated = True
    db.session.add(user)
    db.session.commit()

    new_user = db.session.execute(db.select(User).filter_by(email="testing_user")).scalar_one()
    assert new_user.email == 'testing_user'
    assert not new_user.password_hash == 'test123%'

def test_read_all_users(test_client, init_empty_database):
    """
    GIVEN a database has been initialised with a User table
    WHEN the user entries are queried
    THEN all users are successfully retrieved from the database
    """   

    user_one = User(
        email='jools_user', 
    )
    user_one.set_password('jools123^')
    user_one.authenticated = True

    user_two = User(
        email='fikile_bhele'
    )
    user_two.set_password('fiks123@')
    user_two.authenticated = True

    db.session.add_all([user_one, user_two])
    db.session.commit()

    users_results = db.session.execute(db.select(User.email).order_by(User.email)).all()
    users = [entry for entry in users_results]
    assert len(users) == 2
    assert 'fikile_bhele' in users[0]
    assert 'jools_user' in users[1]

def test_read_all_users_db_empty(init_empty_database):
    """
    GIVEN a database has been initialised with a User table
    WHEN the User table is empty
    AND the User table is queried
    THEN no records are returned
    """    
    users_results = db.session.execute(db.select(User.email).order_by(User.email)).all()
    users = [entry for entry in users_results]
    assert len(users) == 0    

def test_update_user(init_empty_database):
    """
    GIVEN a database has been initialised with a User table
    WHEN an existing user is updated
    THEN the updates are made to the user record in the database
    """ 
    # Create initial record
    user_initial = User(
        email='juliet.doe@gmails.com'
    )
    user_initial.set_password('summ3r!')
    user_initial.authenticated = True
    db.session.add(user_initial)
    db.session.commit()

    new_user = db.session.execute(db.select(User).filter_by(email="juliet.doe@gmails.com")).scalar_one()

    assert new_user.email == 'juliet.doe@gmails.com'

    # Updating record
    new_user.email = 'jeramey.lb.doe@gmails.com'
    db.session.commit()

    updated_user = db.session.execute(db.select(User).filter_by(email="jeramey.lb.doe@gmails.com")).scalar_one()

    assert updated_user.email == 'jeramey.lb.doe@gmails.com'

def test_delete_user(init_empty_database):
    """
    GIVEN a database has been initialised with a User table
    WHEN a record is deleted from the User table
    AND the database is queried for that record
    THEN the User record cannot be retrieved from the database
    """  
    # Create initial record
    user = User(
        email='june.doe@gmails.com'
    )
    user.set_password('junie123!')
    user.authenticated = True
    db.session.add(user)
    db.session.commit()

    new_user = db.session.execute(db.select(User).filter_by(email="june.doe@gmails.com")).scalar_one()

    assert new_user.email == 'june.doe@gmails.com'

    # Actual delete
    db.session.delete(new_user)
    db.session.commit()

    # Verify deletion
    user_post_delete = db.session.execute(db.select(User.email).order_by(User.email)).all()
    remaining_users = [user for user in user_post_delete]
    assert not 'june.doe@gmails.com' in remaining_users

def test_delete_all_users(init_empty_database):
    """
    GIVEN a database has been initialised with a User table
    WHEN all the entries in the User table are deleted
    AND the User table is queried
    THEN no User records are retrieved from the database
    """ 
    user_one = User(
        email='julian.doe@gmails.com'
    )
    user_one.set_password('doe456!')
    user_one.authenticated = True

    user_two = User( 
        email='puleng.khumalo@gmails.com'
    )
    user_two.set_password('khum123$')
    user_two.authenticated = True

    db.session.add_all([user_one, user_two])
    db.session.commit()

    users_results = db.session.execute(db.select(User.email).order_by(User.email)).all()
    users = [entry for entry in users_results]
    assert len(users) == 2

    users_for_delete = db.session.execute(db.select(User).order_by(User.email)).scalars()
    for user in users_for_delete:
        db.session.delete(user)
        db.session.commit()

    users_post_delete = db.session.execute(db.select(User).order_by(User.email)).all()
    users_list = [entry for entry in users_post_delete]
    assert len(users_list) == 0  


# -----------------
# Testing Exceptions
# -----------------
def test_read_member_not_found(init_empty_database):
    """
    GIVEN a database has been initialised with a Member table
    WHEN the database is queried for a member that does not exist
    THEN an exception is raised
    """
    members_results = db.session.execute(db.select(Member.name).order_by(Member.name)).all()
    members = [entry for entry in members_results]
    assert len(members) == 0

    # Assert exception raised for retrieving non-existent member record
    with pytest.raises(NoResultFound):
        new_member = db.session.execute(db.select(Member).filter_by(email="janice.doe@gmails.com")).scalar_one()

def test_update_member_not_found(init_empty_database):
    """
    GIVEN a database has been initialised with a Member table
    WHEN a request is made to update a member record that doesn't exist in the Member table
    THEN an exception is raised
    """        

    member = Member(
        name='Jamie Doe',
        email='jamie.doe@gmails.com'
    )
    db.session.add(member)
    db.session.commit()

    member_to_update = Member(
        name='Dakota Doe',
        email='dakota.doe@gmails.com'
    )

    member_to_update.email = 'd.doe@gmails.com'
    db.session.commit()

    with pytest.raises(NoResultFound):
        member_updated = db.session.execute(db.select(Member).filter_by(email="d.doe@gmails.com")).scalar_one()
        
        assert member_updated.email == 'd.doe@gmails.com'

def test_delete_member_not_found(init_empty_database):
    """
    GIVEN a database has been initialised with a Member table
    WHEN a request is made to delete a member record that doesn't exist in the Member table
    THEN an exception is raised
    """    
    member_to_delete = Member(
        name='Josephine Doe',
        email='josephine.doe@gmails.com'
    )

    with pytest.raises(InvalidRequestError):
        db.session.delete(member_to_delete)
        db.session.commit()

def test_read_user_not_found(init_empty_database):
    """
    GIVEN a database has been initialised with a User table
    WHEN the database is queried for a user record that doesn't exist
    THEN an exception is raised
    """        
    user = User(
        email='testing@users.com"',
    )
    user.set_password('test125%')
    user.authenticated = True
    db.session.add(user)
    db.session.commit()

    with pytest.raises(NoResultFound):
        new_user = db.session.execute(db.select(User).filter_by(email="testingdoe@gmails.com")).scalar_one()

def test_update_user_not_found(init_empty_database):
    """
    GIVEN a database has been initialised with a User table
    WHEN a request is made to update a user record that doesn't exist
    THEN an exception is raised
    """        
    users_results = db.session.execute(db.select(User.email).order_by(User.email)).all()
    users = [entry for entry in users_results]
    assert len(users) == 0

    user = User(
        email='testme@users.com"',
    )
    user.set_password('test1me%')
    user.authenticated = True

    user.email = 'user_test@users.com'
    db.session.commit()

    with pytest.raises(NoResultFound):
        new_user = db.session.execute(db.select(User).filter_by(email="user_test@users.com")).scalar_one()


def test_delete_user_not_found(init_empty_database):
    """
    GIVEN a database has been initialised with a User table
    WHEN a request is made to delete a user record that doesn't exist
    THEN an exception is raised
    """
    user = User(
        email='testing898@users.com"',
    )
    user.set_password('test189%')
    user.authenticated = True

    with pytest.raises(InvalidRequestError):
        db.session.delete(user)
        db.session.commit()
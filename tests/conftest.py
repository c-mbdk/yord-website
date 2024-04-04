import pytest
import os
from datetime import datetime
from sqlalchemy.orm import Session
from yord_website import create_app, db
from yord_website.models import Member, User

@pytest.fixture(scope='module')
def new_member():
    member = Member('Jane Doe', 'jane.doe@gmails.com')
    return member

@pytest.fixture(scope='module')
def new_user():
    user = User(email = 'test_user')
    user.set_password('test123$')
    user.authenticated = True
    return user

@pytest.fixture(scope='module')
def test_client():
    
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    test_flask_app = create_app()

    with test_flask_app.test_client() as testing_client:
        with test_flask_app.app_context():
            yield testing_client

@pytest.fixture(scope='function')
def test_client_request():

    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    test_flask_app = create_app()

    yield test_flask_app          

@pytest.fixture(scope='function')   
def init_database(test_client):
    db.create_all()

    # insert user data
    default_user = User(email = 'test_user')
    default_user.set_password('test123$')
    default_user.authenticated = True
    db.session.add(default_user)

    existing_member = Member('Jane Doe', 'jane.doe@gmails.com')
    db.session.add(existing_member)
    db.session.commit()

    yield

    db.drop_all()

@pytest.fixture(scope='function')
def log_in_default_user(test_client, init_database):
    test_client.post('/auth/login',
                     data={'username': 'test_user', 'password': 'test123$'}) 
    
    yield

    test_client.get('/auth/logout')

@pytest.fixture(scope='function')
def log_in_test_user(test_client):
    test_client.post('/auth/login', data={'email': 'test_user', 'password': 'test123$'})
    yield

    test_client.get('/auth/logout')

@pytest.fixture(scope='module')
def cli_test_client():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    runner = flask_app.test_cli_runner()

    yield runner

@pytest.fixture(scope='function')
def init_empty_database(test_client):
    db.create_all()

    yield
    
    db.drop_all()


# -------------
# Test Data
# -------------
long_name = '22ZkOfNRjg9TCLUQyeYVvPXpNlYLhho4lBPKJcXBPGORpTLMFp303PF0HgWSFQRVpZsVGLFxhMPdYrnxCbPlvIRPv9WGpMyIrnva4'

long_email = 'cusakudouve-7325-189r!r899-fhjkallsdjgoopgaja-dghklnan-AHGKLJ-fahaojlfa_188117a_a8uru0ua;odhafosh891890109i_17fhjajbhaodgahh;lsjdgbajhoiadoisgjda112afajslbfda8901bfa908agpx89auibrb1h08afbofablj1r098r1908fa8adspkhjbga0ahio1ron1j9011ag90dab109g0a@yopmail.com'

long_query = 'cusakudouve-7325-189r!r899-fhjkallsdjgoopgaja-dghklnan-AHGKLJ-fahaojlfa_188117a_a8uru0ua;odhafosh891890109i_17fhjajbhaodgahh;lsjdgbajhoiadoisgjda112afajslbfda8901bfa908agpx89auibrb1h08afbofablj1r098r1908fa8adspkhjbga0ahio1ron1j9011ag90dab109g0a@yopmail.com190iur1u09agua9su[901nlk1098t09-a8s9d0fn1901-'
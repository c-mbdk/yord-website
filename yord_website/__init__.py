from flask import Flask
import os
from flask_wtf.csrf import CSRFProtect
import logging
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler
from click import echo
import sqlalchemy as sa
import pytest

from .extensions import db, login_manager

# -------------
# Configuration
# -------------
csrf_protect = CSRFProtect()
login_manager.login_view = 'auth.login'
BASEDIR = os.path.abspath(os.path.dirname(__file__))
admin_username = f'{os.environ.get("ADMIN_USERNAME")}'
admin_password = f'{os.environ.get("ADMIN_PASSWORD")}'
location_split = BASEDIR.split('/yord_website')
instance_file_location = location_split[0] + '/instance'
test_results = location_split[0] + '/test_results'

# -----------------------------
# Application Factory Function
# -----------------------------
def create_app():
    app = Flask(__name__)

    # Configure the Flask application
    config_type_dev = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type_dev)

    initialise_extensions(app)
    register_blueprints(app)
    configure_logging(app)
    register_cli_commands(app)

    # Check if the database needs to be initialized
    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table("users"):
        with app.app_context():
            db.drop_all()
            from .models import User, Member
            db.create_all()
            user = User(email = admin_username)
            user.set_password(admin_password)
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            app.logger.info('Initialized the database!')
    else:
        app.logger.info('Database already contains the users table.')

    return app

# -----------------
# Helper functions
# -----------------
def initialise_extensions(app):
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        """Given user_id, return the associated User object"""
        return User.query.get(int(user_id))
    

def register_blueprints(app):
    from .auth import auth_routes
    from .mailing import mailing_routes
    from .general import general_routes

    app.register_blueprint(auth_routes.auth_bp, url_prefix='/auth')
    app.register_blueprint(mailing_routes.mailing_bp, url_prefix='/mailing')
    app.register_blueprint(general_routes.general_bp, url_prefix='/general')


def create_instance_log():
    instance_dir_exists = os.path.exists(instance_file_location)

    if not instance_dir_exists:
        os.mkdir(instance_file_location)

    instance_files = os.listdir(instance_file_location)

    if 'yord-website.log' not in instance_files:
        file = open(f'{instance_file_location}/yord-website.log', 'a')
        file.close()       


def configure_logging(app):
    create_instance_log()

    if app.config['LOG_WITH_GUNICORN']:
        gunicorn_error_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.DEBUG)
    else:
        file_handler = RotatingFileHandler(f'{instance_file_location}/yord-website.log',
                                           maxBytes=16384,
                                           backupCount=20)
        file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(threadName)s-%(thread)d: %(message)s [in %(filename)s:%(lineno)d]')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    # Remove the default logger configured by Flask
    app.logger.removeHandler(default_handler)

    app.logger.info('Starting the Flask CFT Yord Website App...')
    

def register_cli_commands(app):
    @app.cli.command('init_db')
    def initialise_database():
        db.drop_all()
        db.create_all()
        echo('Initialized the database!')

    @app.cli.command()
    def test():
        """Runs all tests."""
        echo('Running all tests and producing an XML report...')
        exit(pytest.main(["-s", "--minpass=86", "--junit-xml=test_results/junit.xml", 'tests']))
        

    @app.cli.command()
    def unittest():
        """Runs all unit tests."""    
        pytest.main(["-s", "--cov=yord_website", 'tests/unit/'])
        echo('All unit tests have been run.')

    @app.cli.command()
    def functionaltest():
        """Runs all functional tests."""    
        pytest.main(["-s", "--cov=yord_website", 'tests/functional/'])
        echo('All functional tests have been run.')

    # Run tests and generate HTML reports
    @app.cli.command()
    def testhtml():
       """Runs all tests and generates a HTML report."""
       pytest.main(["-s", "--cov", "--cov-report=html:test_coverage_reports", 'tests'])    
       echo('All tests have been run and an HTML report has been generated.')     
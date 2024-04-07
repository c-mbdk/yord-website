"""
This file (test_cli.py) contains the functional tests for the CLI (Command-Line Interface) functions.
"""

import pytest


def test_initialize_database(cli_test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the 'flask init_db' command is called from the command line
    THEN a relevant confirmation message will be outputted
    """
    output = cli_test_client.invoke(args=['init_db'])
    assert output.exit_code == 0
    assert 'Initialized the database!' in output.output

def test_run_all_tests(cli_test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the 'flask test' command is called from the command line
    THEN a relevant confirmation message will be outputted
    """    
    output = cli_test_client.invoke(args=['test'])
    assert output.exit_code == 0
    assert 'All tests have been run and an XML report produced.' in output.output

@pytest.mark.skip(reason="takes too long to run")
def test_run_unit_tests(cli_test_client):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the 'flask unittest' command is called from the command line
    THEN a relevant confirmation message will be outputted
    """
    output = cli_test_client.invoke(args=['unittest'])
    assert output.exit_code == 0
    assert 'All unit tests have been run.' in output.output   
     
@pytest.mark.skip(reason="takes too long to run")     
def test_run_functional_tests(cli_test_client):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the 'flask funcitonaltest' command is called from the command line
    THEN a relevant confirmation message will be outputted
    """
    output = cli_test_client.invoke(args=['functionaltest'])
    assert output.exit_code == 0
    assert 'All functional tests have been run.' in output.output    

@pytest.mark.skip(reason="takes too long to run")
def test_run_all_tests_with_html_report(cli_test_client):
    """
    GIVEN a Flask application has been configured for testing
    WHEN the 'flask testhtml' command is called from the command line
    THEN a relevant confirmation message will be outputted
    """
    output = cli_test_client.invoke(args=['testhtml'])
    assert output.exit_code == 0
    assert 'All tests have been run and an HTML report has been generated.' in output.output           
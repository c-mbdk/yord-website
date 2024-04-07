# yord-website

## About this project
This project initially focused on mailing list management for a church youth group. You could sign up to the mailing list from the landing page and then view the current members on the mailing list. The functionality also included being able to edit member details and delete members from the mailing list. The mailing list was also visible and editable by all.

The latest iteration of this project includes:
- basic authentication: only logged in users can view and edit the mailing list
- forms with validation: this includes the login form, the mailing list registration form and the contact form
- navigation bar: the mailing list option is only available if you're signed in, otherwise the 'log in' option is visible, alongside the other pages
- new pages: contact us, about, gallery
- tests: unit and functional tests with coverage
- logs
- automated deployment: a YAML file to run a build, test and deploy pipeline with CircleCI
- a YAML file to run a test pipeline with GitHub Actions

## What's next?
Over the course of upgrading this project, a backlog of features was naturally built. Some features started off as must-haves, some were swapped out for 'quick fixes' i.e., unfortunately introducing tech debt and some only became obvious during the implementation/testing. This is the backlog for features/changes to the test suite:
- Adding a confirmation dialog for deleting mailing list members
- Configuring the contact us form to actually send emails
- Adding videos to the gallery
- Using a page range instead of 'Page X of X'
- Routing requests for 'unauthorised' actions to a specific page (e.g., attempts to view/edit the mailing list whilst not being logged in)
- UI tests
- Fix the individual form unit tests to support the 'InputRequired' validator
- Displaying the sign-up error directly on the sign-up page
- Making more of the site responsive


## How to Run Locally

1. Install virtualenv:
```
$ pip install virtualenv
```

2. Open a terminal in the project root directory and run:
```
$ virtualenv env
```

3. Then run the command:

Windows
```
$ .\env\Scripts\activate
```

Mac
```
$ source env/bin/activate
```

4. Then install the dependencies:
```
$ (env) pip install -r requirements.txt
```

5. Finally, start the web server:
```
$ (env) python3 app.py
```

6. This server will start on port 5000 by default. You can change this by adding the 'port' parameter in the following line in app.py like this:
```
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)
```

## Running the tests

Before running any tests, ensure that you are in the root directory and in the virtual environment i.e., same level as the app.py file.

To run a specific file, ensure that you are in the root directory and then run this command:
```
python3 -m pytest tests/<filename>/test_<file>.py
```

For example, to run just the tests for the 'General' blueprint, run this command:
```
python3 -m pytest tests/functional/test_general.py
```

The application has a few custom commands for running tests. To run all the tests, you can use this command:
```
flask test
```

The other custom commands for running tests are detailed in the `__init__.py` file in the yord_website subdirectory. 
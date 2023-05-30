# yord-website

## About this project
This project focuses on mailing list management for a church youth group. People can sign up to the mailing list from the landing page. There is a separate page to view the current members on the mailing list. Member details can be edited and members can also be deleted from the mailing list. 

Currently, the mailing list is visible to all users. A future release will include authentication, only allowing specific users to view the mailing list. 

## How to Run

1. Install virtualenv:
```
$ pip install virtualenv
```

2. Open a terminal in the project root directory and run:
```
$ virtualenv env
```

3. Then run the command:
```
$ .\env\Scripts\activate
```

4. Then install the dependencies:
```
$ (env) pip install -r requirements.txt
```

5. Finally, start the web server:
```
$ (env) python app.py
```

6. This server will start on port 5000 by default. You can change this by updating the following line in app.py to this:
```
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)
```


from flask import Flask, url_for, render_template, request, redirect, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'fyu78gof9q8rhf9sa8a0/'
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mailinglist.db"
db.init_app(app)
app.app_context().push()


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(320), nullable=False)
    email = db.Column(db.String(320), nullable=False, unique=True)
    date_added = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def __repr__(self):
        return f'Member {self.id}'

# @app.route('/')
# def index():
#     render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_entry = Member(name=name, email=email)

        # checking if member already exists
        email_in_db = Member.query.filter_by(email=email).first()
        if email_in_db is not None:
            flash("This email is already registered!")
        
        else:
            try:
                db.session.add(new_entry)
                db.session.commit()
                flash("Confirmed! You're in!")
                return render_template('index.html')
            except:
                return 'There was an error submitting your details.'
        
    return render_template('index.html')

@app.route('/mailing', methods=['POST', 'GET'])
def mailing():
    if request.method == 'GET':
        members = Member.query.order_by(Member.date_added).all()
        return render_template('mailing.html', members=members)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    member = Member.query.get_or_404(id)

    if request.method == 'POST':
        member.name = request.form['name']
        member.email = request.form['email']

        try:
            db.session.commit()
            return redirect('/mailing')
        except:
            return "There was an issue updating this member's details"

    else:
        return render_template('edit.html', member=member)

@app.route('/delete/<int:id>')
def delete(id):
    member_to_remove = Member.query.get_or_404(id)
    
    try:
        db.session.delete(member_to_remove)
        db.session.commit()
        return redirect('/mailing')
    except:
        return "There was an issue removing this member from the mailing list"

if __name__ == "__main__":
    app.run(debug=True)
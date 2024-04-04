from flask import Blueprint, render_template, request, redirect, url_for
from yord_website.extensions import db
from yord_website.models import Member, RegistrationForm, ContactForm

general_bp = Blueprint(
    'general', __name__,
    template_folder='templates',
    url_prefix='/general'
)

@general_bp.route('/home', methods=['POST', 'GET'])
def home():
    form = RegistrationForm()
    
    if request.method == 'GET':
       return render_template('general/index.html', form=form)
    
    else:
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
        
            member = Member.query.filter_by(email=email).first()
            if member is not None:
                email_registered_alert = True
                return render_template('general/index.html', form=form, email_registered_alert=email_registered_alert)

            try:
                new_entry = Member(name=name, email=email)
                db.session.add(new_entry)
                db.session.commit()
                return redirect(url_for('general.confirm_signup'))  
            except:
                return redirect(url_for('general.error_signup'))      


@general_bp.route('/confirm', methods=['GET'])
def confirm_signup():
    """Confirmation of sign up to Mailing List Page"""
    
    return render_template('general/confirm-signup.html')

@general_bp.route('/about', methods=['GET'])
def about():
    """About Page"""
    return render_template('general/about.html')


@general_bp.route('/contact', methods=["GET", "POST"])
def contact():
    """Contact Page"""
    form = ContactForm()

    return render_template('general/contact.html', form=form)

@general_bp.route('gallery', methods=["GET"])
def gallery():
    """Gallery Page"""
    return render_template('general/gallery.html')

@general_bp.route('error')
def error_signup():
    """Error Page for failed mailing list registration"""
    return render_template('general/error-signup.html')
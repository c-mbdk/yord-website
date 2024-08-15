from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import login_required
from yord_website.extensions import db
from yord_website.models import Member, EditMemberDetailsForm

mailing_bp = Blueprint(
    'mailing', __name__,
    template_folder='templates'
)


@mailing_bp.route('/members', methods=['GET', 'POST'])
@login_required
def view_members():
    page = request.args.get('page', 1, type=int)
    members_query = db.session.scalars(db.select(Member).order_by(Member.date_added)).all()

    per_page = current_app.config['MEMBERS_PER_PAGE']
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(members_query) + per_page - 1) // per_page
    
    members = members_query[start:end]
    
    return render_template('mailing/members.html', members=members, total_pages=total_pages, page=page)

@mailing_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_member(id):
    member = db.session.get(Member, id)

    if member is None:
        return redirect(url_for('mailing.view_members'))

    form = EditMemberDetailsForm(obj = db.session.get(Member, id))

    if request.method == 'POST':
        if form.validate_on_submit():
            member.name = form.name.data
            member.email = form.email.data

            try:
                db.session.commit()
                return redirect(url_for('mailing.view_members'))
            except:
                error_updating_member = True
                return render_template('mailing/edit.html', member=member, form=form, error_updating_member=error_updating_member)
        
        else:
            error_updating_member = True
            return render_template('mailing/edit.html', member=member, form=form, error_updating_member=error_updating_member)    
    else:
        return render_template('mailing/edit.html', member=member, form=form)

    
@mailing_bp.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    member_to_remove = db.session.get(Member, id)
    
    try:
        db.session.delete(member_to_remove)
        db.session.commit()
        return redirect(url_for('mailing.view_members'))
    except:
        error_deleting_member = True
        return render_template('mailing/members.html', error_deleting_member=error_deleting_member)
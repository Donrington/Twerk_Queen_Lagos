import json, os
import io
import  secrets
from os.path import basename
import random
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from flask_login import current_user, login_required
from flask import * 
from markupsafe import escape
import re 
from flask_wtf.csrf import CSRFProtect, generate_csrf
from app import *
from main.forms import *
from main.models import *
from flask_login import login_required
from main.models import db
from sqlalchemy import func,desc  
from datetime import datetime, timedelta
import pytz


def init_routes(app):
    @app.route('/')
    def index():
        # Query to get all contestants and their votes
        finalists = Contestant.query.filter_by(finalist=True).all()
        posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_on.desc()).all()
        contestant_votes = []
        for contestant in finalists:
            vote_count = Vote.query.filter_by(contestant_id=contestant.id).count()
            contestant_votes.append({
                "name": contestant.first_name + " " + contestant.last_name,
                "photo": contestant.passport_photo,
                "vote_count": vote_count,
                "id": contestant.id
            })

        return render_template('user/index.html', contestant_votes=contestant_votes, posts=posts, pagename="TwerkQueenLagos | Homepage")

    @app.route('/aboutus')
    def aboutus():
        posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_on.desc()).all()
        return render_template('user/aboutus.html', pagename="TwerkQueenLagos | About", posts=posts)

    # Add to your routes.py
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            try:
                name = request.form['name']
                email = request.form['email']
                message = request.form['message']
                
                new_message = ContactMessage(
                    name=name,
                    email=email,
                    message=message
                )
                
                db.session.add(new_message)
                db.session.commit()
                flash('Your message has been sent successfully!', 'success')
                return redirect(url_for('contact'))
                
            except Exception as e:
                db.session.rollback()
                flash('Error sending message. Please try again.', 'error')
                return redirect(url_for('contact'))
        
        return render_template('user/contactus.html', pagename="TwerkQueenLagos | Contact")



    @app.route('/weeklyaudition')
    def weeklyaudition():
        return render_template('user/weeklyaud.html', pagename="TwerkQueenLagos | Weekly Audition")


   
   
# Set the maximum file size (2MB) for security purposes
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB file size limit

    # Ensure upload directory exists
    if not os.path.exists(app.config['USER_PROFILE_PATH']):
        os.makedirs(app.config['USER_PROFILE_PATH'])

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    def allowed_file(filename):
        
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Error handler to catch requests with large files
    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(error):
        flash('File too large! Maximum allowed size is 2MB.', 'danger')
        # Redirect back to the registration form or a relevant page
        return redirect(url_for('register'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            # Retrieve form fields and strip spaces
            first_name = request.form.get('first-name', '').strip()
            last_name = request.form.get('last-name', '').strip()
            email = request.form.get('email', '').strip()
            state_of_origin = request.form.get('state', '').strip()
            date_of_birth = request.form.get('dob', '').strip()
            passport_photo = request.files.get('image')

            # Validate form fields
            if not first_name or not last_name or not email or not state_of_origin or not date_of_birth:
                flash('All fields are required.', 'danger')
                return redirect(url_for('register'))

            # Check if email already exists
            existing_contestant = Contestant.query.filter_by(email=email).first()
            if existing_contestant:
                flash('Email already registered. Please use a different email.', 'danger')
                return redirect(url_for('register'))

            # Validate date format
            try:
                date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d")
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
                return redirect(url_for('register'))

            # Handle file upload
            if not passport_photo:
                flash('Please upload a passport photo.', 'danger')
                return redirect(url_for('register'))

            if passport_photo and allowed_file(passport_photo.filename):
                # Secure the filename
                photo_filename = secure_filename(passport_photo.filename)
                file_path = os.path.join(app.config['USER_PROFILE_PATH'], photo_filename)

                # Since Flask will already catch files >2MB (due to MAX_CONTENT_LENGTH),
                # the following manual file size check is only reached for valid sizes.
                passport_photo.seek(0, os.SEEK_END)
                file_size = passport_photo.tell()
                passport_photo.seek(0)

                if file_size > app.config['MAX_CONTENT_LENGTH']:
                    flash('File too large! Maximum allowed size is 2MB.', 'danger')
                    return redirect(url_for('register'))

                passport_photo.save(file_path)
                passport_photo_path = f"static/uploads/{photo_filename}"
            else:
                flash('Invalid passport photo. Only JPG, PNG under 2MB are allowed.', 'danger')
                return redirect(url_for('register'))

            # Save contestant to the database
            new_contestant = Contestant(
                first_name=first_name,
                last_name=last_name,
                email=email,
                state_of_origin=state_of_origin,
                date_of_birth=date_of_birth,
                passport_photo=passport_photo_path,
                registered_on=datetime.utcnow()
            )

            db.session.add(new_contestant)
            db.session.commit()

            flash('Registration successful! You are now in the contest.', 'success')
            return redirect(url_for('registration_success'))
        
        return render_template('user/register.html', pagename="TwerkQeenLagos | Registration")

    
    
    @app.route('/blog')
    def blog():
        admin = Admin.query.get(session.get('id'))
        posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_on.desc()).all()
        return render_template('user/blog.html', posts=posts, admin=admin,pagename="TwerkQueenLagos | Blog & News")
    

    @app.route('/blog/<slug>')
    def post_detail(slug):
        post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
        return render_template('user/blogdetails.html', post=post, pagename=f"TwerkQueenLagos | {post.title}")
        
    @app.route('/eliminate')
    def eliminate():
        return render_template('user/eliminate_rd.html', pagename="TwerkQueenLagos | Elinimation ROunds")
    
    @app.route('/dashboard')
    def dashboard():
        return render_template('user/admindash.html', pagename="TwerkQueenLagos | Dashboard")
    


    # Define custom Jinja filter
    def replace_spaces(value):
        return value.replace(' ', '').lower()

    app.jinja_env.filters['replace_spaces'] = replace_spaces


import json, os
import io
import  secrets
from os.path import basename
import random
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from flask import * 
from markupsafe import escape
import re 
from flask_wtf.csrf import CSRFProtect, generate_csrf
from app import *
from main import *
from main.forms import *
from main.models import *
from PIL import Image
from flask_login import login_required
from main.models import db
from sqlalchemy import func,desc  
from datetime import datetime, timedelta
import pytz





def init_routes(app):
    @app.route('/admin/dashboard')
    @admin_login_required
    def admin_dashboard():
        # Fetch logged-in admin details
        admin = Admin.query.get(session.get('id'))
        if not admin:
            flash('Admin not found.', 'danger')
            return redirect(url_for('admin_login'))

        # Fetch dynamic data from the database
        total_contestants = Contestant.query.count()
        total_votes = Vote.query.count()
        active_blog_posts = BlogPost.query.filter_by(is_published=True).count()
        new_contacts = ContactMessage.query.filter_by(is_resolved=False).count()

        return render_template(
            'user/admindash.html', 
            pagname="Admin Dashboard", 
            admin=admin, 
            total_contestants=total_contestants,
            total_votes=total_votes,
            active_blog_posts=active_blog_posts,
            new_contacts=new_contacts
        )
    
    @app.route('/admin/users')
    def admin_users():
        return render_template('user/users.html', paagname="Manage Users")

  
    
  

    @app.route('/admin/register/', methods=['GET', 'POST'])
    def admin_register():
        errors = {}
        if request.method == 'POST':
            # Retrieve form data
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            email = request.form.get('email')

            # Basic validation
            if not username:
                errors['username'] = 'Username is required.'
            if not email:
                errors['email'] = 'Email is required.'
            if not password:
                errors['password'] = 'Password is required.'
            if password != confirm_password:
                errors['confirm_password'] = 'Passwords do not match.'

            # Check if username or email already exists
            if Admin.query.filter_by(username=username).first():
                errors['username'] = 'Username already exists.'
            if Admin.query.filter_by(email=email).first():
                errors['email'] = 'Email already registered.'

            if errors:
                # Render template with errors
                return render_template('user/adminreg.html', errors=errors, request=request)
            else:
                # Create new admin
                admin = Admin(username=username, email=email)
                admin.set_password(password)
                db.session.add(admin)
                db.session.commit()
                flash('Admin registered successfully. You can now log in.')
                return redirect(url_for('admin_login'))

        return render_template('user/adminreg.html', errors=errors, request=request)


        
    @app.route('/admin/login/', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            admin = Admin.query.filter_by(username=username).first()

            if admin and admin.check_password(password):
                session['admin_logged_in'] = True
                session['id'] = admin.id
                session['username'] = admin.username
                session['avatar'] = admin.avatar  # Store avatar in session
                flash('Admin logged in successfully.')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password.', 'danger')

        return render_template('user/adminlogin.html')

    @app.route('/admin/logout/')
    def admin_logout():
        session.pop('admin_logged_in', None)
        session.pop('id', None)
        session.pop('username', None)  # Remove username from session
        flash('Admin logged out.')
        return redirect(url_for('admin_login'))



    # Ensure the upload directory exists
    if not os.path.exists(app.config['ADMIN_PROFILE_PATH']):
        os.makedirs(app.config['ADMIN_PROFILE_PATH'])

    # ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # def allowed_file(filename):
    #     """Check if the file extension is allowed."""
    #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # @app.route('/admin/profile', methods=['POST'])
    # @admin_login_required
    # def upload_avatar():
    #     if 'avatar' not in request.files or request.files['avatar'].filename == '':
    #         flash('No file uploaded.', 'danger')
    #         return redirect(url_for('admin_dashboard'))

    #     file = request.files['avatar']
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         file_path = os.path.join(app.config['ADMIN_PROFILE_PATH'], filename)
    #         file.save(file_path)

    #         # Update the admin's avatar in the database
    #         admin = Admin.query.get(session['id'])
    #         if admin:
    #             admin.avatar = f"/{app.config['ADMIN_PROFILE_PATH']}/{filename}"  # Store relative path
    #             db.session.commit()

    #             # Update session
    #             session['avatar'] = admin.avatar

    #             flash('Avatar updated successfully.', 'success')
    #         else:
    #             flash('Admin not found.', 'danger')

    #         return redirect(url_for('admin_dashboard'))

    #     flash('Invalid file type. Allowed: png, jpg, jpeg, gif.', 'danger')
    #     return redirect(url_for('admin_dashboard'))
        
    @app.before_request
    def set_csrf_token():
        """Ensure a CSRF token exists in the session before handling requests."""
        if "_csrf_token" not in session:
            session["_csrf_token"] = secrets.token_hex(16)  # Generate CSRF token


    @app.route('/admin/set_finalist/<int:contestant_id>', methods=['POST'])
    @csrf.exempt
    @admin_login_required
    def set_finalist(contestant_id):
        """Sets or removes a contestant as a finalist."""
        if 'id' not in session:
            return jsonify({"error": "Unauthorized"}), 403  

        contestant = Contestant.query.get(contestant_id)
        if not contestant:
            return jsonify({"error": "Contestant not found"}), 404

        # Ensure request contains JSON data
        if not request.is_json:
            return jsonify({"error": "Invalid request format. Expected JSON."}), 400  

        data = request.get_json()
        if "status" not in data:
            return jsonify({"error": "Missing 'status' field in request."}), 400  

        try:
            contestant.finalist = bool(data["status"])
            db.session.commit()
            return jsonify({"success": True, "message": f"{contestant.first_name} is now a {'Finalist' if contestant.finalist else 'Regular Contestant'}."}), 200
        except Exception as e:
            db.session.rollback()
            print(f"Error setting finalist: {e}")  # Log error
            return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

    @app.route('/admin/contestants')
    @admin_login_required
    def admin_contestants():
        """Retrieve all contestants and display them in the admin panel."""
        admin = Admin.query.get(session.get('id'))  # Ensure admin is logged in
        if not admin:
            flash('Admin not found.', 'danger')
            return redirect(url_for('admin_login'))

        contestants = Contestant.query.order_by(Contestant.registered_on.desc()).all()
        
        return render_template('user/contestants.html', paagname="Contestants", admin=admin, contestants=contestants)

    @app.route('/admin/delete_contestant/<int:contestant_id>', methods=['POST'])
    @admin_login_required
    def delete_contestant(contestant_id):
        contestant = Contestant.query.get_or_404(contestant_id)
        
        # Remove contestant's photo from the filesystem (optional)
        if contestant.passport_photo:
            photo_path = os.path.join(app.config['USER_PROFILE_PATH'], os.path.basename(contestant.passport_photo))
            if os.path.exists(photo_path):
                os.remove(photo_path)

        # Delete contestant from the database
        db.session.delete(contestant)
        db.session.commit()

        flash("Contestant deleted successfully!", "success")
        return redirect(url_for('admin_dashboard'))


      
    @app.route('/admin/votes')
    @admin_login_required
    def admin_votes():
        admin = Admin.query.get(session.get('id'))
        if 'id' not in session:
            return redirect(url_for('admin_login'))  # Redirect to homepage if not an admin

        # Query to get all contestants and their votes
        contestants = Contestant.query.all()
        
        # For each contestant, we count the number of votes
        contestant_votes = []
        for contestant in contestants:
            vote_count = Vote.query.filter_by(contestant_id=contestant.id).count()
            contestant_votes.append({
                "name": contestant.first_name + " " + contestant.last_name,
                "vote_count": vote_count,
                "id": contestant.id
            })

        # Render the admin votes page with contestant vote data
        return render_template('user/contestant_votes.html', contestant_votes=contestant_votes, admin=admin, paagname="TwerkQueenLagos | Contestant Votes") 


    @app.route('/update_vote_count/<int:contestant_id>', methods=['POST'])
    @admin_login_required
    def update_vote_count(contestant_id):
        try:
            if 'id' not in session:
                return jsonify({"error": "Unauthorized"}), 403

            contestant = Contestant.query.get(contestant_id)
            if not contestant:
                return jsonify({"error": "Contestant not found"}), 404

            data = request.get_json()
            number_of_votes = data.get('number_of_votes', 0)  # Default to 0

            # Ensure it's an integer
            try:
                number_of_votes = int(number_of_votes)
            except ValueError:
                return jsonify({"error": "Invalid vote count"}), 400

            # Fetch current votes count
            current_vote_count = Vote.query.filter_by(contestant_id=contestant.id).count()

            # Handle addition of votes
            if number_of_votes > 0:
                for _ in range(number_of_votes):
                    new_vote = Vote(contestant_id=contestant.id)
                    db.session.add(new_vote)

            # Handle subtraction of votes
            elif number_of_votes < 0:
                votes_to_remove = min(abs(number_of_votes), current_vote_count)  # Ensure we don't remove more votes than available
                
                if votes_to_remove > 0:
                    votes = Vote.query.filter_by(contestant_id=contestant.id).limit(votes_to_remove).all()
                    for vote in votes:
                        db.session.delete(vote)

            db.session.commit()

            # Get the updated vote count
            updated_vote_count = Vote.query.filter_by(contestant_id=contestant.id).count()

            return jsonify({"success": True, "new_vote_count": updated_vote_count})

        except Exception as e:
            db.session.rollback()
            print(f"Error updating votes: {str(e)}")  # Log the actual error
            return jsonify({"error": "Internal Server Error", "details": str(e)}), 500



    @app.route('/admin/blog')
    @admin_login_required
    @csrf.exempt
    def admin_blog():
        """List all blog posts (admin view)."""
        admin = Admin.query.get(session.get('id'))
        posts = BlogPost.query.order_by(BlogPost.created_on.desc()).all()
        return render_template('user/adminblog.html', posts=posts, admin=admin)

    @app.route('/admin/blog/new', methods=['GET', 'POST'])
    @admin_login_required
    @csrf.exempt
    def admin_blog_new():
        """Create a new blog post."""
        admin = Admin.query.get(session.get('id'))
        if request.method == 'POST':
            title = request.form.get('title')
            slug = request.form.get('slug')
            content = request.form.get('content')
            author = request.form.get('author', 'Admin')
            image_url = request.form.get('image_url', '')
            is_published = bool(request.form.get('is_published'))

            if not title or not slug or not content:
                flash('Title, slug, and content are required.', 'danger')
                return redirect(url_for('admin_blog_new'))

            new_post = BlogPost(
                title=title,
                slug=slug,
                content=content,
                author=author,
                image_url=image_url,
                is_published=is_published
            )
            db.session.add(new_post)
            db.session.commit()
            flash('Blog post created successfully!', 'success')
            return redirect(url_for('admin_blog'))

        return render_template('user/adminblog_new.html', admin=admin)

    @app.route('/admin/blog/edit/<int:post_id>', methods=['GET', 'POST'])
    @admin_login_required
    @csrf.exempt
    def admin_blog_edit(post_id):
        """Edit an existing blog post."""
        admin = Admin.query.get(session.get('id'))
        post = BlogPost.query.get_or_404(post_id)

        if request.method == 'POST':
            post.title = request.form.get('title')
            post.slug = request.form.get('slug')
            post.content = request.form.get('content')
            post.author = request.form.get('author', 'Admin')
            post.image_url = request.form.get('image_url', '')
            post.is_published = bool(request.form.get('is_published'))
            post.updated_on = datetime.utcnow()

            db.session.commit()
            flash('Blog post updated successfully!', 'success')
            return redirect(url_for('admin_blog'))

        return render_template('user/admin_blog_edit.html', post=post, admin=admin)

    @app.route('/admin/blog/delete/<int:post_id>', methods=['POST'])
    @admin_login_required
    @csrf.exempt
    def admin_blog_delete(post_id):
        """Delete a blog post."""
        post = BlogPost.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        flash('Blog post deleted.', 'info')
        return redirect(url_for('admin_blog'))

       # Admin route for viewing messages
    @app.route('/admin/contacts')
    @admin_login_required # Assuming you have admin authentication
    def admin_contacts():
        admin = Admin.query.get(session.get('id'))
        page = request.args.get('page', 1, type=int)
        messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).paginate(page=page, per_page=10)
        return render_template('user/admincontact.html', messages=messages, admin=admin, pagename="Contact Messages")
       


    @app.route('/admin/message/<int:message_id>')
    @admin_login_required
    def view_message(message_id):
        admin = Admin.query.get(session.get('id'))
        message = ContactMessage.query.get_or_404(message_id)
        return render_template('user/view_message.html', message=message, admin=admin)

    @app.route('/admin/toggle-resolved/<int:message_id>', methods=['POST'])
    @admin_login_required
    @csrf.exempt
    def toggle_resolved(message_id):
        message = ContactMessage.query.get_or_404(message_id)
        message.is_resolved = not message.is_resolved
        db.session.commit()
        flash('Message status updated', 'success')
        return redirect(url_for('admin_contacts'))


    @app.route('/admin/settings', methods=['GET', 'POST'])
    @admin_login_required
    def admin_settings():
        admin = Admin.query.get(session.get('id'))

        if request.method == 'POST':
            updated = False  # Track if any changes were made

            # Handle username and email update
            new_username = request.form.get('username')
            new_email = request.form.get('email')

            if new_username and new_username != admin.username:
                if Admin.query.filter_by(username=new_username).first():
                    flash('Username is already taken', 'error')
                else:
                    admin.username = new_username
                    updated = True

            if new_email and new_email != admin.email:
                if Admin.query.filter_by(email=new_email).first():
                    flash('Email is already in use', 'error')
                else:
                    admin.email = new_email
                    updated = True

            # Handle avatar upload
            if 'avatar' in request.files:
                avatar = request.files['avatar']
                if avatar.filename != '':
                    if not allowed_file(avatar.filename):
                        flash('Invalid file type', 'error')
                    else:
                        filename = secure_filename(avatar.filename)
                        upload_folder = os.path.join(app.config['ADMIN_PROFILE_PATH'], 'avatars')
                        os.makedirs(upload_folder, exist_ok=True)
                        avatar_path = os.path.join(upload_folder, filename)

                        try:
                            with Image.open(avatar) as img:
                                img.thumbnail((300, 300))
                                img.save(avatar_path)
                                admin.avatar = f"uploads/admins/avatars/{filename}"
                                updated = True
                        except Exception as e:
                            flash('Error processing image', 'error')

            # Handle password change
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            if new_password or confirm_password:
                if not current_password:
                    flash('Current password is required to change your password', 'error')
                elif new_password != confirm_password:
                    flash('New passwords do not match', 'error')
                elif not admin.check_password(current_password):
                    flash('Current password is incorrect', 'error')
                else:
                    admin.set_password(new_password)
                    updated = True
                    flash('Password updated successfully', 'success')

            if updated:
                db.session.commit()
                flash('Settings updated successfully', 'success')
            else:
                flash('No changes made', 'info')

            return redirect(url_for('admin_settings'))

        return render_template('user/admin_settings.html', 
                                pagename="Account Settings",  
                                admin=admin)

    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
   
    @app.route('/update-dark-mode', methods=['POST'])
    @admin_login_required
    def update_dark_mode():
        session['dark_mode'] = request.json.get('dark_mode', False)
        return jsonify(success=True)

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in as an admin.')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function
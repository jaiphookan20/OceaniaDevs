from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from extensions import bcrypt, db
from models import Seeker

auth_blueprint = Blueprint('auth', __name__)

# Registration route:
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name').strip()
        last_name = request.form.get('last_name').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password')
        city = request.form.get('city').strip()
        state = request.form['state'].strip()
        country = request.form['country'].strip()

        # Check if user already exists
        user_exists = Seeker.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered.')
            return redirect(url_for('auth.register'))
        
        # Hash the password and print it for verification
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # print(f"Generated hash for password '{password}': {hashed_password}")

        # Create a new seeker object
        new_seeker = Seeker(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=hashed_password,  # Save the hashed password
            city=city,
            state=state,
            country=country
        )
        db.session.add(new_seeker)
        db.session.commit()

        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    else:
        return render_template('register.html')

# Login route for seekers:
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        seeker = Seeker.query.filter_by(email=email).first()

        if seeker:
            if seeker.verify_password(password):
                # session['user_id'] = {"uid": seeker.uid, "email": seeker.email}
                session['user_id'] = seeker.uid
                # print('Session after login:', session, "session user_id:", session['user_id'], "user id in session:", "user_id" in session)
                # print(session.get('user_id')["email"])
                # session_type = current_app.config.get('SESSION_TYPE')
                # print("session_type: ", session_type)
                return redirect(url_for('home'))  # Redirect to a home page instead of rendering
            else:
                flash('Invalid password. Please try again.')
        else:
            flash('No account found with that email.')

        return redirect(url_for('auth.login'))  # Always redirect after form submission
    else:  # If it's a GET request, render the login page
        return render_template('login.html')

# Logout route for seekers:
@auth_blueprint.route('/logout')
def logout():
    print('Current session before clearing:', session)
    session.clear()
    print('Session after clearing:', session)
    return redirect(url_for('auth.login'))
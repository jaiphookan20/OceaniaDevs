from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import bcrypt, db
from models import Seeker

auth_blueprint = Blueprint('auth', __name__)

# Registration route:
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # If it's a POST request (form submission)
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        city = request.form.get('city')
        state = request.form['state']
        country = request.form['country']

        # Check if user already exists
        user_exists =  Seeker.query.filter_by(email=email).first()
        if user_exists:
            # If user exists, flash a message and redirect to the registration page
            flash('Email already registered.')
            return redirect(url_for('auth.register'))

        # Create a new seeker object
        new_seeker =  Seeker(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=bcrypt.generate_password_hash(password).decode('utf-8'),  # Hash the password
            city=city,
            state=state,
            country=country
        )
        # Add the new seeker to the database session and commit
        db.session.add(new_seeker)
        db.session.commit()

        # Flash a success message and redirect to the login page
        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    else:  # If it's a GET request (rendering the registration page)
        return render_template('register.html')

# Login route for seekers:
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        seeker = Seeker.query.filter_by(email=email).first()

        # Debugging output
        if seeker:
            print(f"Seeker found: {seeker.email}")
        else:
            print("No seeker found with that email.")

        if seeker and seeker.verify_password(password):
                session['user_id'] = seeker.uid
                print('Session Set:', session['user_id'])
                flash('Login successful!')
                print('Login successful!')
                return render_template('index.html')
        else:
            flash('No seeker found with that email or password doesnt match')
            print('No seeker found with that email or password doesnt match')
            return redirect(url_for('auth.login'))  # Redirect back to login if no seeker found
    else:  # If it's a GET request, render the login page
        return render_template('login.html')

# Logout route for seekers:
@auth_blueprint.route('/logout')
def logout():
    print('Current session before clearing:', session)
    session.clear()
    print('Session after clearing:', session)
    return redirect(url_for('auth.login'))
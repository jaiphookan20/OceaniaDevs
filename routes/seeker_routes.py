from flask import Blueprint, render_template, request, redirect, url_for, session
from service.seeker_service import SeekerService

seeker_blueprint = Blueprint('seeker', __name__)

# Add Job Seeker Route
@seeker_blueprint.route('/add_seeker', methods=['GET', 'POST'])
def add_seeker():
    if request.method == 'POST':
        # Extract form data and call the add_seeker method of SeekerService
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']

        seeker_service = SeekerService() 
        seeker_service.add_seeker(first_name, last_name, email, city, state, country)

        return "Job Seeker added successfully!"
    else:
        return render_template('add_seeker.html')



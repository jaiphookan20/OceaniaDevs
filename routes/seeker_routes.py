from flask import Blueprint, render_template, request, redirect, url_for, session,jsonify
from service.seeker_service import SeekerService
from models import Seeker

seeker_blueprint = Blueprint('seeker', __name__)

# Add Job Seeker Route
@seeker_blueprint.route('/add_seeker', methods=['GET', 'POST'])
def update_seeker():
    if request.method == 'POST':
        if 'user' not in session:
            print('user not in session, cannot update Seeker')
            return jsonify({"error": "Unauthorized access"}), 401

        # Extract form data and call the update_seeker method of SeekerService
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        
        seeker_service = SeekerService() 
        seeker_service.update_seeker(first_name, last_name, city, state, country)

        return "Job Seeker Updated successfully!"
    else:
        return render_template('add_seeker.html')



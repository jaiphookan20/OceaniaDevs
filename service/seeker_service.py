from models import Seeker
from flask import session
from extensions import db
class SeekerService:

    def update_seeker(self, first_name, last_name, city, state, country):
        """
        Update Seeker Details in the Seekers table
        """
        # Extract Logged In User's Email from Session
        user_email = session.get('user').get('userinfo').get('email')
        # Extract Seeker Row to Update using Email
        seeker = Seeker.query.filter_by(email=user_email).first()
        
        if seeker:
            seeker.first_name = first_name
            seeker.last_name = last_name
            seeker.city = city
            seeker.state = state
            seeker.country = country
            db.session.commit()
            print('Seeker Details Updated Successfully!')
            return True
        print('No Seeker Found with provided credentials')
        return False
    
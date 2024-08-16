from models import Seeker, Application, Bookmark
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
    
    def get_all_applied_jobs_by_seeker(self, userid):
        """
        Return all applied jobs by userID.
        :param userid: int - ID of the user who applied for the job.
        """
        return Application.query.filter_by(userid=userid).all()
    
    # def get_all_bookmarked_jobs_by_seeker(self, userid):
    #     """
    #     Return all bookmarked jobs by userID.
    #     :param userid: int - ID of the user who applied for the job.
    #     """
    #     return Bookmark.query.filter_by(userid=userid).all()

    def get_all_bookmarked_jobs_by_seeker(self, userid, page, page_size):
        """
        Return all bookmarked jobs by userID with pagination, sorted by most recent first.
        :param userid: int - ID of the user who bookmarked the job.
        :param page: int - Page number.
        :param page_size: int - Number of items per page.
        """
        return Bookmark.query.filter_by(userid=userid).order_by(Bookmark.datetimestamp.desc()).paginate(page=page, per_page=page_size, error_out=False).items

    def update_application_status(self, application_id, new_status):
        """
        Update the status of an application.
        :param application_id: int - ID of the application to update.
        :param new_status: str - New status for the application.
        :return: bool - True if update was successful, False otherwise.
        """
        try:
            application = Application.query.get(application_id)
            if not application:
                return False
            
            application.status = new_status
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error updating application status: {str(e)}")
            db.session.rollback()
            return False
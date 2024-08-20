from models import Seeker, Application, Bookmark
from flask import session
from extensions import db
class SeekerService:

    def get_seeker_by_id(self, seeker_id):
        return Seeker.query.get(seeker_id)

    def update_seeker(self, seeker_id, data):
        seeker = self.get_seeker_by_id(seeker_id)
        if seeker:
            seeker.first_name = data.get('firstName', seeker.first_name)
            seeker.last_name = data.get('lastName', seeker.last_name)
            seeker.city = data.get('city', seeker.city)
            seeker.state = data.get('state', seeker.state)
            seeker.country = data.get('country', seeker.country)
            
            try:
                db.session.commit()
                return True
            except Exception as e:
                print(f"Error updating seeker info: {str(e)}")
                db.session.rollback()
                return False
        return False
    
    # With Pagination
    def get_all_applied_jobs_by_seeker(self, userid, page, page_size):
        """
        Return all applied jobs by userID with pagination, sorted by most recent first.
        :param userid: int - ID of the user who applied for the job.
        :param page: int - Page number.
        :param page_size: int - Number of items per page.
        """
        return Application.query.filter_by(userid=userid).order_by(Application.datetimestamp.desc()).paginate(page=page, per_page=page_size, error_out=False).items

    # No Pagination
    def get_user_applications(self, userid):
        """
        Return all applied jobs by userID with pagination, sorted by most recent first.
        :param userid: int - ID of the user who applied for the job.
        :param page: int - Page number.
        :param page_size: int - Number of items per page.
        """
        return Application.query.filter_by(userid=userid).order_by(Application.datetimestamp.desc());
    
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
        

    def remove_bookmark(self, userid, jobid):
        """
        Remove a bookmark for a specific user and job.
        :param userid: int - ID of the user.
        :param jobid: int - ID of the job.
        :return: bool - True if removal was successful, False otherwise.
        """
        try:
            bookmark = Bookmark.query.filter_by(userid=userid, jobid=jobid).first()
            if bookmark:
                db.session.delete(bookmark)
                db.session.commit()
                return True
            return False
        except Exception as e:
            print(f"Error removing bookmark: {str(e)}")
            db.session.rollback()
            return False
        
    
    def remove_application(self, userid, jobid):
        """
        Remove an application for a specific user and job.
        :param userid: int - ID of the user.
        :param jobid: int - ID of the job.
        :return: bool - True if removal was successful, False otherwise.
        """
        try:
            application = Application.query.filter_by(userid=userid, jobid=jobid).first()
            if application:
                db.session.delete(application)
                db.session.commit()
                return True
            return False
        except Exception as e:
            print(f"Error removing application: {str(e)}")
            db.session.rollback()
            return False
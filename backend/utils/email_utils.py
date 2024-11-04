from flask_mail import Message
from flask import current_app
from extensions import mail

def send_scraper_report(scraper_name: str, stats: dict, errors: list):
    """Send email report after scraper completion"""
    try:
        subject = f"{scraper_name} Scraper Report"
        
        # Create HTML content with statistics
        html_content = f"""
        <h2>{scraper_name} Scraper Results</h2>
        <h3>Statistics:</h3>
        <ul>
            <li>Total jobs scraped: {stats.get('total_scraped', 0)}</li>
            <li>Successfully added: {stats.get('successfully_added', 0)}</li>
            <li>Skipped (existing): {stats.get('skipped_existing', 0)}</li>
            <li>Failed: {stats.get('failed', 0)}</li>
        </ul>
        """
        
        # Add errors section if there are any
        if errors:
            html_content += f"""
            <h3>Errors ({len(errors)}):</h3>
            <ul>
                {''.join(f'<li>{error}</li>' for error in errors[:10])}
            </ul>
            """
            if len(errors) > 10:
                html_content += f"<p>... and {len(errors) - 10} more errors</p>"
        
        msg = Message(
            subject=subject,
            recipients=['jaiphookan@gmail.com'],
            html=html_content
        )
        
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email report: {str(e)}")
        return False
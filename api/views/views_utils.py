from django.conf import settings
from datetime import datetime
from django.core.mail import EmailMultiAlternatives

def get_current_period(all_periods):
    """
    Returns the current period for a cooperative id based on today date.
    """
    today = datetime.today()
    # Note that if there are two periods that overlap, it returns the last one.
    periods = [period for period in all_periods if
                        datetime.strptime(period['date_from'], '%Y-%m-%d') <= today <= datetime.strptime(
                            period['date_to'], '%Y-%m-%d')]
    if periods: 
        return periods[len(periods) - 1]
    return None

def create_and_send_email(subject, text_content, html_content, destination_emails):
    email = EmailMultiAlternatives(subject, text_content,
                                    getattr(settings, "EMAIL_FROM_ACCOUNT", "test@console.com"),
                                    destination_emails)    
    email.content_subtype = "html"
    email.attach_alternative(html_content, "text/html")
    email.send()
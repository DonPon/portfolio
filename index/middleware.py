import requests
from datetime import timedelta, datetime
from django.utils import timezone
from .models import Visitor
from django.utils.deprecation import MiddlewareMixin
from django.core.mail import send_mail
import os
from dotenv import load_dotenv
import textwrap
# Load environment variables from .env file
load_dotenv()

class LogVisitorMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get the user's IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # Get the user agent (browser and OS information)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Check if the IP was logged within the last hour
        last_hour = timezone.now() - timedelta(hours=1)
        existing_visitor = Visitor.objects.filter(ip_address=ip, visit_time__gte=last_hour).exists()

        if not existing_visitor:
            # Fetch geolocation data
            geo_response = requests.get(f'http://ip-api.com/json/{ip}')
            geo_data = geo_response.json()

            if geo_response.status_code == 200 and geo_data.get('status') == 'success':
                city = geo_data.get('city')
                region = geo_data.get('regionName')
                country = geo_data.get('country')
            else:
                city = region = country = None

            # Save the visitor information to the database
            Visitor.objects.create(
                ip_address=ip,
                user_agent=user_agent,
                city=city,
                region=region,
                country=country,
            )

            # Prepare visitor details for the email
            visitor_details = f"""
            IP Address: {ip}
            User Agent: {user_agent}
            City: {city}
            Region: {region}
            Country: {country}
            At: {datetime.now().strftime('%d/%m/%y - %H:%M')}"""

            # Get email credentials from environment variables
            email_host_user = os.getenv('EMAIL_HOST_USER')
            email_host_password = os.getenv('EMAIL_HOST_PASSWORD')
            recipient_email = os.getenv('RECIPIENT_EMAIL')

            # Send an email with the visitor's details
            send_mail(
                subject='New Visitor Logged to Portfolio',
                message=f'A new visitor was logged to your portfolio:\n\n{textwrap.dedent(visitor_details)}',
                from_email=email_host_user,
                recipient_list=[recipient_email],
                fail_silently=False,
            )

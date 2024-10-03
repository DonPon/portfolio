import requests
from datetime import timedelta
from django.utils import timezone
from .models import Visitor
from django.utils.deprecation import MiddlewareMixin

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

        # Check if the IP was logged within the last hour (for example)
        last_hour = timezone.now() - timedelta(hours=1)
        existing_visitor = Visitor.objects.filter(ip_address=ip, visit_time__gte=last_hour).exists()

        if not existing_visitor:
            # Fetch geolocation data
            geo_response = requests.get(f'http://ip-api.com/json/{ip}')
            geo_data = geo_response.json()

            # Only proceed if the request was successful and valid
            if geo_response.status_code == 200 and geo_data.get('status') == 'success':
                city = geo_data.get('city')
                region = geo_data.get('regionName')
                country = geo_data.get('country')

            else:
                city = region = country = None
                latitude = longitude = None

            # Save the visitor information to the database
            Visitor.objects.create(
                ip_address=ip,
                user_agent=user_agent,
                city=city,
                region=region,
                country=country,
            )

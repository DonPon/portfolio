# index/views.py
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib import messages
from .models import PortfolioItem
from .forms import ContactForm
from dotenv import load_dotenv
from django.core.mail import send_mail
import os
import textwrap
# Load environment variables from .env file
load_dotenv()

class PortfolioListView(ListView):
    model = PortfolioItem
    template_name = 'index/portfolio.html'  # Specify your own template name/location
    context_object_name = 'items'  # Default is 'object_list', we change it to 'items'

class ContactFormView(FormView):
    template_name = 'index/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')  # Redirects to the same page on success

    def form_valid(self, form):
        # Save the form data to the database
        form.save()

        # Get the submitted data
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')

        # Prepare the email content
        email_subject = 'New Contact Form Submission'
        email_body = f"""
        You have received a new message from your portfolio website contact form:

        Name: {name}
        Email: {email}
        Message: 
        {message}
        """

        # Get email credentials from environment variables
        email_host_user = os.getenv('EMAIL_HOST_USER')
        recipient_email = os.getenv('RECIPIENT_EMAIL')

        # Send the email
        send_mail(
            subject=email_subject,
            message=textwrap.dedent(email_body),
            from_email=email_host_user,
            recipient_list=[recipient_email],
            fail_silently=False,
        )

        # Display a success message on the website
        messages.success(self.request, "Your message has been sent!")

        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle form errors
        messages.error(self.request, "There was an error with your submission.")
        return super().form_invalid(form)
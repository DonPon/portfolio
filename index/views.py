# index/views.py
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib import messages
from .models import PortfolioItem
from .forms import ContactForm


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
        messages.success(self.request, "Your message has been sent!")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle form errors
        messages.error(self.request, "There was an error with your submission.")
        return super().form_invalid(form)
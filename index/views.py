# index/views.py

from django.views.generic import ListView
from .models import PortfolioItem

class PortfolioListView(ListView):
    model = PortfolioItem
    template_name = 'index/portfolio.html'  # Specify your own template name/location
    context_object_name = 'items'  # Default is 'object_list', we change it to 'items'


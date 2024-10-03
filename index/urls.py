# index/urls.py

from django.urls import path
from index.views import PortfolioListView, ContactFormView

urlpatterns = [
    path('', PortfolioListView.as_view(), name='portfolio'),
    path('contact/', ContactFormView.as_view(), name='contact'),
]
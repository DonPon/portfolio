# index/urls.py

from django.urls import path
from index.views import PortfolioListView

urlpatterns = [
    path('', PortfolioListView.as_view(), name='portfolio'),
]
# index/admin.py

from django.contrib import admin
from .models import PortfolioItem, Contact, Visitor

admin.site.register(PortfolioItem)
admin.site.register(Contact)
admin.site.register(Visitor)
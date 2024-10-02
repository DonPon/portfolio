# index/models.py

from django.db import models

class PortfolioItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='')
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title
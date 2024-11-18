from django.db import models
from django.utils import timezone

class Keyword(models.Model):
    name = models.CharField(max_length=200)
    search_volume = models.IntegerField()
    difficulty = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)  # Field to store creation time
    updated_at = models.DateTimeField(auto_now=True)      # Field to store last update time
    favorite = models.BooleanField(default=False)  # New field to mark as favorite

    def __str__(self):
        return self.name
    
from django.db import models

class Review(models.Model):
    review_text = models.TextField()
    rating = models.IntegerField(null=True, blank=True)  # Optional rating
    date = models.DateField(auto_now_add=True)
    source = models.CharField(max_length=100, blank=True, null=True)  # e.g., platform name

    def __str__(self):
        return f"Review {self.id} - Sentiment Analysis"

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    reviews = models.IntegerField()
    sales = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
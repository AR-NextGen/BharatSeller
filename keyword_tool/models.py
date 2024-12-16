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
    
from django.db import models

class Keyword(models.Model):
    keyword = models.CharField(max_length=255, default='default_keyword')
    category = models.CharField(max_length=255, choices=[
        ('Mobiles, Computers', 'Mobiles, Computers'),
        ('TV, Appliances, Electronics', 'TV, Appliances, Electronics'),
        ("Men's Fashion", "Men's Fashion"),
        ("Women's Fashion", "Women's Fashion"),
        ('Home, Kitchen, Pets', 'Home, Kitchen, Pets'),
        ('Beauty, Health, Grocery', 'Beauty, Health, Grocery'),
        ('Sports, Fitness, Bags, Luggage', 'Sports, Fitness, Bags, Luggage'),
        ("Toys, Baby Products, Kids' Fashion", "Toys, Baby Products, Kids' Fashion"),
        ('Car, Motorbike, Industrial', 'Car, Motorbike, Industrial'),
        ('Books', 'Books'),
        ('Movies, Music & Video Games', 'Movies, Music & Video Games'),
    ],default='Uncategorized')
    search_volume = models.IntegerField(default=0)
    sales = models.IntegerField(default=0)
    sponsored_asin = models.CharField(max_length=255, blank=True, null=True)
    match_type = models.CharField(max_length=50, blank=True, null=True)
    suggested_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.keyword
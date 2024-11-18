from django import forms
from .models import Keyword

class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ['name', 'search_volume', 'difficulty']

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

from django import forms

class ProductSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    category = forms.CharField(max_length=255, required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    min_rating = forms.DecimalField(max_digits=3, decimal_places=2, required=False)
    max_rating = forms.DecimalField(max_digits=3, decimal_places=2, required=False)
    min_reviews = forms.IntegerField(required=False)
    max_reviews = forms.IntegerField(required=False)
    min_sales = forms.IntegerField(required=False)
    max_sales = forms.IntegerField(required=False)

    from django import forms

class ProductSearchForm(forms.Form):
    SORT_CHOICES = [
        ('name', 'Name'),
        ('price', 'Price'),
        ('rating', 'Rating'),
        ('reviews', 'Reviews'),
        ('sales', 'Sales'),
    ]

    name = forms.CharField(max_length=255, required=False)
    category = forms.CharField(max_length=255, required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    min_rating = forms.DecimalField(max_digits=3, decimal_places=2, required=False)
    max_rating = forms.DecimalField(max_digits=3, decimal_places=2, required=False)
    min_reviews = forms.IntegerField(required=False)
    max_reviews = forms.IntegerField(required=False)
    min_sales = forms.IntegerField(required=False)
    max_sales = forms.IntegerField(required=False)
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False)


from django import forms

class SimplifiedProductSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    category = forms.CharField(max_length=255, required=False)

from django import forms

CATEGORY_CHOICES = [
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
]

from django import forms

CATEGORY_CHOICES = [
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
]

class ProductSearchForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)
    improvements = forms.CharField(max_length=255, required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    min_rating = forms.DecimalField(max_digits=3, decimal_places=2, required=False)
    max_rating = forms.DecimalField(max_digits=3, decimal_places=2, required=False)
    min_reviews = forms.IntegerField(required=False)
    max_reviews = forms.IntegerField(required=False)
    min_sales = forms.IntegerField(required=False)
    max_sales = forms.IntegerField(required=False)
    sort_by = forms.ChoiceField(choices=[
        ('category', 'Category'),
        ('price', 'Price'),
        ('rating', 'Rating'),
        ('reviews', 'Reviews'),
        ('sales', 'Sales'),
    ], required=False)

class SimplifiedProductSearchForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)
    improvements = forms.CharField(max_length=255, required=False)
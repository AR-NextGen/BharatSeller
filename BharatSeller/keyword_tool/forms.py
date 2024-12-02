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
    name = forms.CharField(max_length=255, required=False)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    min_rating = forms.DecimalField(max_digits=3, decimal_places=2, required=False)
    max_rating = forms.DecimalField(max_digits=3, decimal_places=2, required=False)
    min_reviews = forms.IntegerField(required=False)
    max_reviews = forms.IntegerField(required=False)
    min_sales = forms.IntegerField(required=False)
    max_sales = forms.IntegerField(required=False)
    sort_by = forms.ChoiceField(choices=[
        ('name', 'Name'),
        ('price', 'Price'),
        ('rating', 'Rating'),
        ('reviews', 'Reviews'),
        ('sales', 'Sales'),
    ], required=False)

class SimplifiedProductSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)

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

class KeywordAnalysisForm(forms.Form):
    keyword = forms.CharField(max_length=255, required=True)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True)

from django import forms

class KeywordOptimizationForm(forms.Form):
    keywords = forms.CharField(widget=forms.Textarea, required=True, help_text="Enter keywords separated by commas or new lines.")
    remove_duplicates = forms.BooleanField(required=False, initial=True)
    maintain_phrases = forms.BooleanField(required=False, initial=True)
    protect_numbers = forms.BooleanField(required=False, initial=True)
    convert_to_lowercase = forms.BooleanField(required=False, initial=True)
    add_comma_with_spaces = forms.BooleanField(required=False, initial=False)
    add_comma_without_spaces = forms.BooleanField(required=False, initial=False)
    include_word_frequency = forms.BooleanField(required=False, initial=False)
    remove_common_words = forms.BooleanField(required=False, initial=False)
    remove_single_letter_words = forms.BooleanField(required=False, initial=False)
    replace_word = forms.CharField(max_length=255, required=False, help_text="Enter a word to replace.")
    replace_with = forms.CharField(max_length=255, required=False, help_text="Enter the replacement word.")


# Feild 1 to search ASINs
from django import forms

class CerebroForm(forms.Form):
    asins = forms.CharField(
        max_length=50,  # 5 ASINs * 10 characters each
        required=True,
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter ASINs',
            'class': 'form-control form-control-lg asin-input',  # Add custom class for styling
            'data-toggle': 'tooltip',
            'title': 'Enter up to 5 ASINs, separated by commas.'
        })
    )

from django import forms

class FetchListingForm(forms.Form):
    asin = forms.CharField(
        max_length=10,
        required=True,
        label='ASIN',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter ASIN',
            'class': 'form-control'
        })
    )

class CreateListingForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=True,
        label='Title',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Title',
            'class': 'form-control'
        })
    )
    description = forms.CharField(
        required=True,
        label='Description',
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter Description',
            'class': 'form-control',
            'rows': 3
        })
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        label='Price',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter Price',
            'class': 'form-control'
        })
    )
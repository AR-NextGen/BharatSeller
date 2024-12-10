from django import forms
from .models import Keyword
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Review Analysis Form
class ReviewAnalysisForm(forms.Form):
    identifier = forms.CharField(
        label='ASIN or URL', 
        max_length=255, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter ASIN or URL', 'class': 'form-control'})  
    )

# Register Form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# Product Explorer Form with Sorting
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

IMPROVEMENT_CHOICES = [
    ('', 'Level'),
    ('Slight', 'Slight'),
    ('Moderate', 'Moderate'),
    ('Significant', 'Significant'),
]

class ProductexplorerForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)
    improvements = forms.ChoiceField(choices=IMPROVEMENT_CHOICES, required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    min_rating = forms.DecimalField(max_digits=3, decimal_places=2, required=False)
    max_rating = forms.DecimalField(max_digits=3, decimal_places=2, required=False)
    min_reviews = forms.IntegerField(required=False)
    max_reviews = forms.IntegerField(required=False)
    min_sales = forms.IntegerField(required=False)
    max_sales = forms.IntegerField(required=False)
    min_revenue = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_revenue = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    shipping_size_tier = forms.CharField(max_length=255, required=False)
    bsr = forms.IntegerField(required=False)

# Simplified Product Explorer Form
class SimplifiedProductexplorerForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)
    improvements = forms.ChoiceField(choices=IMPROVEMENT_CHOICES, required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    competition = forms.ChoiceField(choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], required=False)

# Keyword Forge Form
class KeywordForgeForm(forms.ModelForm):
    keyword = forms.CharField(required=False, label='Keyword Search')

    class Meta:
        model = Keyword
        fields = ['keyword', 'category']

# Key Cleanse Form
class KeyCleanseForm(forms.Form):
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

# Spy Glass Form
class SpyGlassForm(forms.Form):
    asins = forms.CharField(
        max_length=50,  
        required=True,
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter ASINs',
            'class': 'form-control form-control-lg asin-input',  
            'data-toggle': 'tooltip',
            'title': 'Enter up to 5 ASINs, separated by commas.'
        })
    )

# Fetch Listing Form
class FetchListingForm(forms.Form):
    asin = forms.CharField(
        max_length=255,
        required=True,
        label='ASIN or URL',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter ASIN or URL',
            'class': 'form-control'
        })
    )

# Create Listing Form
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

# Sales Guesstimator Form
class SalesGuesstimatorForm(forms.Form):
    product_asin = forms.CharField(
        max_length=10,
        required=False,
        label='Product ASIN',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Product ASIN',
            'class': 'form-control'
        })
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False,
        label='Category',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

# Listing Booster Form
class ListingBoosterForm(forms.Form):
    main_listing = forms.CharField(
        label='Main Listing', 
        max_length=255, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter ASIN or URL'})  
    )
    competitor_listing = forms.CharField(
        label='Competitor Listing', 
        max_length=255, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "Enter Competitor's ASIN or URL"})  
    )

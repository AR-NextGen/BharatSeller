from django.shortcuts import render, redirect
from .models import Keyword
from .forms import KeywordForm
from django.core.paginator import Paginator


from django.db.models import F
from django.contrib.auth.decorators import login_required

@login_required
def keyword_list(request):
    sort_by = request.GET.get("sort", "name")
    keywords = Keyword.objects.all().order_by(sort_by)
    query = request.GET.get("q")
    not_found_message = None

    if query:
        keywords = keywords.filter(name__icontains=query)
        if not keywords.exists():
            not_found_message = "Word not found."

    # Set up pagination: Show 5 keywords per page
    paginator = Paginator(keywords, 5)  # Change 5 to any number of items you want per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "keyword_tool/keyword_list.html", {
        "page_obj": page_obj,
        "not_found_message": not_found_message,
    })





# New view to add a new keyword
def add_keyword(request):
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('keyword_list')  # Redirect to keyword list after saving
    else:
        form = KeywordForm()
    
    return render(request, 'keyword_tool/add_keyword.html', {'form': form})

from django.shortcuts import redirect, get_object_or_404

def delete_keyword(request, keyword_id):
    keyword = get_object_or_404(Keyword, id=keyword_id)  # Fetch keyword by ID
    keyword.delete()                                     # Delete the keyword
    return redirect('keyword_list')                      # Redirect to keyword list

from django.shortcuts import get_object_or_404, redirect

# New view for editing a keyword
def edit_keyword(request, keyword_id):
    keyword = get_object_or_404(Keyword, id=keyword_id)
    if request.method == 'POST':
        print("Received data:", request.POST)  # Debug line to show POST data
        keyword.name = request.POST['name']
        keyword.search_volume = request.POST['search_volume']
        keyword.difficulty = request.POST['difficulty']
        keyword.save()
        print("Updated keyword difficulty:", keyword.difficulty)  # Confirm saved value
        return redirect('keyword_list')
    return render(request, 'keyword_tool/edit_keyword.html', {'keyword': keyword})


from django.shortcuts import render, get_object_or_404

def keyword_detail(request, keyword_id):
    keyword = get_object_or_404(Keyword, id=keyword_id)
    return render(request, 'keyword_tool/keyword_detail.html', {'keyword': keyword})

from django.shortcuts import get_object_or_404, redirect
from .models import Keyword

def toggle_favorite(request, keyword_id):
    keyword = get_object_or_404(Keyword, id=keyword_id)
    keyword.favorite = not keyword.favorite  # Toggle the favorite status
    keyword.save()
    return redirect('keyword_list')

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration
            return redirect('keyword_list')  # Redirect to the keyword list or any other page
    else:
        form = UserCreationForm()
    return render(request, 'keyword_tool/register.html', {'form': form})

from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user right after registration
            return redirect("keyword_list")  # Redirect to the keyword list page after registration
    else:
        form = RegisterForm()
    return render(request, "keyword_tool/register.html", {"form": form})

import matplotlib
matplotlib.use('Agg')

from django.shortcuts import render
from textblob import TextBlob
import matplotlib.pyplot as plt
import io
import urllib, base64

def review_analysis(request):
    analysis_result = None
    polarity_scores = []
    subjectivity_scores = []

    if request.method == 'POST':
        review_text = request.POST.get('review')
        if review_text:
            # Split input text into multiple sentences for analysis
            reviews = review_text.split(".")
            
            for review in reviews:
                analysis = TextBlob(review)
                polarity_scores.append(analysis.sentiment.polarity)
                subjectivity_scores.append(analysis.sentiment.subjectivity)

        # Generate polarity histogram
        fig, ax = plt.subplots()
        ax.hist(polarity_scores, bins=10, color='skyblue', edgecolor='black')
        ax.set_title('Sentiment Polarity Distribution')
        ax.set_xlabel('Polarity')
        ax.set_ylabel('Frequency')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        histogram_url = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close(fig)

        # Generate subjectivity pie chart
        subjective_count = sum(1 for score in subjectivity_scores if score >= 0.5)
        objective_count = len(subjectivity_scores) - subjective_count
        fig, ax = plt.subplots()
        ax.pie([subjective_count, objective_count], labels=['Subjective', 'Objective'], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        pie_chart_url = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close(fig)

        # Pass generated chart URLs to template
        analysis_result = {
            'histogram_url': histogram_url,
            'pie_chart_url': pie_chart_url,
            'polarity_scores': polarity_scores,
            'subjectivity_scores': subjectivity_scores,
        }
        
    # Render the template, even if no POST data is available
    return render(request, 'keyword_tool/review_analysis.html', {'analysis_result': analysis_result})


# import matplotlib
# matplotlib.use('Agg')

# from django.shortcuts import render
# from textblob import TextBlob
# import matplotlib.pyplot as plt
# import io
# import base64
# from textblob import Word
# from django.http import JsonResponse

# def review_analysis(request):
#     analysis_result = None
#     polarity_scores = []
#     subjectivity_scores = []
#     highlighted_text = ""

#     if request.method == 'POST':
#         review_text = request.POST.get('review')
#         if review_text:
#             # Split input text into multiple sentences for better analysis granularity
#             reviews = review_text.split(".")

#             for review in reviews:
#                 analysis = TextBlob(review)
#                 polarity_scores.append(analysis.sentiment.polarity)
#                 subjectivity_scores.append(analysis.sentiment.subjectivity)

#             # Extract keywords and apply highlighting based on polarity
#             words = TextBlob(review_text).words
#             keywords = []
#             for word in words:
#                 word_blob = TextBlob(word)
#                 word_polarity = word_blob.sentiment.polarity
#                 if abs(word_polarity) > 0.2:
#                     keywords.append((word, "positive" if word_polarity > 0 else "negative"))

#             for word, sentiment in keywords:
#                 if sentiment == "positive":
#                     highlighted_text += f'<span style="color:green; font-weight:bold;">{word}</span> '
#                 elif sentiment == "negative":
#                     highlighted_text += f'<span style="color:red; font-weight:bold;">{word}</span> '
#                 else:
#                     highlighted_text += word + " "

#         # Generate histogram for polarity distribution
#         fig, ax = plt.subplots()
#         ax.hist(polarity_scores, bins=10, color='skyblue', edgecolor='black')
#         ax.set_title('Sentiment Polarity Distribution')
#         ax.set_xlabel('Polarity')
#         ax.set_ylabel('Frequency')

#         # Convert histogram to base64 image
#         buf = io.BytesIO()
#         plt.savefig(buf, format='png')
#         buf.seek(0)
#         histogram_url = base64.b64encode(buf.getvalue()).decode('utf-8')
#         buf.close()
#         plt.close(fig)

#         # Generate pie chart for subjectivity distribution
#         subjective_count = sum(1 for score in subjectivity_scores if score >= 0.5)
#         objective_count = len(subjectivity_scores) - subjective_count
#         fig, ax = plt.subplots()
#         ax.pie([subjective_count, objective_count], labels=['Subjective', 'Objective'],
#                autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightcoral'])
#         ax.axis('equal')

#         # Convert pie chart to base64 image
#         buf = io.BytesIO()
#         plt.savefig(buf, format='png')
#         buf.seek(0)
#         pie_chart_url = base64.b64encode(buf.getvalue()).decode('utf-8')
#         buf.close()
#         plt.close(fig)

#         # Compile analysis results for template rendering
#         analysis_result = {
#             'histogram_url': histogram_url,
#             'pie_chart_url': pie_chart_url,
#             'polarity_scores': polarity_scores,
#             'subjectivity_scores': subjectivity_scores,
#             'highlighted_text': highlighted_text,
#         }

#     return render(request, 'keyword_tool/review_analysis.html', {'analysis_result': analysis_result})

from django.shortcuts import render
from textblob import TextBlob
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def review_analysis(request):
    if request.method == 'POST':
        review_text = request.POST.get('review')
        if review_text:
            try:
                analysis = TextBlob(review_text)
                polarity = analysis.sentiment.polarity
                subjectivity = analysis.sentiment.subjectivity
                analysis_result = {
                    'review_text': review_text,
                    'polarity': polarity,
                    'subjectivity': subjectivity,
                }
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse(analysis_result)
                return render(request, 'keyword_tool/review_analysis.html', {'analysis_result': analysis_result})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    return render(request, 'keyword_tool/review_analysis.html')

# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import Product
# from .forms import ProductSearchForm

# def product_search(request):
#     form = ProductSearchForm(request.GET or None)
#     products = Product.objects.all()

#     if form.is_valid():
#         if form.cleaned_data['name']:
#             products = products.filter(name__icontains=form.cleaned_data['name'])
#         if form.cleaned_data['category']:
#             products = products.filter(category__icontains=form.cleaned_data['category'])
#         if form.cleaned_data['min_price']:
#             products = products.filter(price__gte=form.cleaned_data['min_price'])
#         if form.cleaned_data['max_price']:
#             products = products.filter(price__lte=form.cleaned_data['max_price'])
#         if form.cleaned_data['min_rating']:
#             products = products.filter(rating__gte=form.cleaned_data['min_rating'])
#         if form.cleaned_data['max_rating']:
#             products = products.filter(rating__lte=form.cleaned_data['max_rating'])
#         if form.cleaned_data['min_reviews']:
#             products = products.filter(reviews__gte=form.cleaned_data['min_reviews'])
#         if form.cleaned_data['max_reviews']:
#             products = products.filter(reviews__lte=form.cleaned_data['max_reviews'])
#         if form.cleaned_data['min_sales']:
#             products = products.filter(sales__gte=form.cleaned_data['min_sales'])
#         if form.cleaned_data['max_sales']:
#             products = products.filter(sales__lte=form.cleaned_data['max_sales'])
            

#     return render(request, 'keyword_tool/product_search.html', {'form': form, 'products': products})

from django.shortcuts import render
from django.http import JsonResponse
from .models import Product
from .forms import ProductSearchForm, SimplifiedProductSearchForm
from django.core.paginator import Paginator

def product_search(request):
    advanced_form = ProductSearchForm(request.GET or None)
    simplified_form = SimplifiedProductSearchForm(request.GET or None)
    products = Product.objects.all()

    if 'advanced' in request.GET:
        form = advanced_form
        if form.is_valid():
            if form.cleaned_data['category']:
                products = products.filter(category__icontains=form.cleaned_data['category'])
            if form.cleaned_data['improvements']:
                products = products.filter(improvements__icontains=form.cleaned_data['improvements'])
            if form.cleaned_data['min_price']:
                products = products.filter(price__gte=form.cleaned_data['min_price'])
            if form.cleaned_data['max_price']:
                products = products.filter(price__lte=form.cleaned_data['max_price'])
            if form.cleaned_data['min_rating']:
                products = products.filter(rating__gte=form.cleaned_data['min_rating'])
            if form.cleaned_data['max_rating']:
                products = products.filter(rating__lte=form.cleaned_data['max_rating'])
            if form.cleaned_data['min_reviews']:
                products = products.filter(reviews__gte=form.cleaned_data['min_reviews'])
            if form.cleaned_data['max_reviews']:
                products = products.filter(reviews__lte=form.cleaned_data['max_reviews'])
            if form.cleaned_data['min_sales']:
                products = products.filter(sales__gte=form.cleaned_data['min_sales'])
            if form.cleaned_data['max_sales']:
                products = products.filter(sales__lte=form.cleaned_data['max_sales'])
            if form.cleaned_data['sort_by']:
                products = products.order_by(form.cleaned_data['sort_by'])
    else:
        form = simplified_form
        if form.is_valid():
            if form.cleaned_data['category']:
                products = products.filter(category__icontains=form.cleaned_data['category'])
            if form.cleaned_data['improvements']:
                products = products.filter(improvements__icontains=form.cleaned_data['improvements'])

    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'products': list(page_obj.object_list.values()), 'has_next': page_obj.has_next(), 'has_previous': page_obj.has_previous(), 'num_pages': page_obj.paginator.num_pages, 'current_page': page_obj.number})

    return render(request, 'keyword_tool/product_search.html', {'advanced_form': advanced_form, 'simplified_form': simplified_form, 'products': page_obj, 'is_advanced': 'advanced' in request.GET})
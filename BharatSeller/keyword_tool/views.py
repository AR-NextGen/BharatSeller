from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Keyword, KeywordAnalysis, Product
from .forms import KeywordForm, RegisterForm, ProductSearchForm, SimplifiedProductSearchForm, KeywordAnalysisForm
import matplotlib
matplotlib.use('Agg')
from textblob import TextBlob
import matplotlib.pyplot as plt
import io
import urllib, base64

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

    paginator = Paginator(keywords, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "keyword_tool/keyword_list.html", {
        "page_obj": page_obj,
        "not_found_message": not_found_message,
    })

def delete_keyword(request, keyword_id):
    keyword = get_object_or_404(Keyword, id=keyword_id)
    keyword.delete()
    return redirect('keyword_list')

def edit_keyword(request, keyword_id):
    keyword = get_object_or_404(Keyword, id=keyword_id)
    if request.method == 'POST':
        keyword.name = request.POST['name']
        keyword.search_volume = request.POST['search_volume']
        keyword.difficulty = request.POST['difficulty']
        keyword.save()
        return redirect('keyword_list')
    return render(request, 'keyword_tool/edit_keyword.html', {'keyword': keyword})

def keyword_detail(request, keyword_id):
    keyword = get_object_or_404(Keyword, id=keyword_id)
    return render(request, 'keyword_tool/keyword_detail.html', {'keyword': keyword})

def toggle_favorite(request, keyword_id):
    keyword = get_object_or_404(Keyword, id=keyword_id)
    keyword.favorite = not keyword.favorite
    keyword.save()
    return redirect('keyword_list')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'keyword_tool/register.html', {'form': form})

def test_login_template(request):
    return render(request, 'keyword_tool/login.html')

def review_analysis(request):
    analysis_result = None
    polarity_scores = []
    subjectivity_scores = []

    if request.method == 'POST':
        review_text = request.POST.get('review')
        if review_text:
            reviews = review_text.split(".")
            for review in reviews:
                analysis = TextBlob(review)
                polarity_scores.append(analysis.sentiment.polarity)
                subjectivity_scores.append(analysis.sentiment.subjectivity)

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

        subjective_count = sum(1 for score in subjectivity_scores if score >= 0.5)
        objective_count = len(subjectivity_scores) - subjective_count
        fig, ax = plt.subplots()
        ax.pie([subjective_count, objective_count], labels=['Subjective', 'Objective'], autopct='%1.1%f%%', startangle=90)
        ax.axis('equal')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        pie_chart_url = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close(fig)

        analysis_result = {
            'histogram_url': histogram_url,
            'pie_chart_url': pie_chart_url,
            'polarity_scores': polarity_scores,
            'subjectivity_scores': subjectivity_scores,
        }
        
    return render(request, 'keyword_tool/review_analysis.html', {'analysis_result': analysis_result})

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

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'products': list(page_obj.object_list.values()), 'has_next': page_obj.has_next(), 'has_previous': page_obj.has_previous(), 'num_pages': page_obj.paginator.num_pages, 'current_page': page_obj.number})

    return render(request, 'keyword_tool/product_search.html', {'advanced_form': advanced_form, 'simplified_form': simplified_form, 'products': page_obj, 'is_advanced': 'advanced' in request.GET})

def home(request):
    return render(request, 'keyword_tool/home.html')

def keyword_analysis(request):
    form = KeywordAnalysisForm(request.GET or None)
    results = None

    if form.is_valid():
        keyword = form.cleaned_data['keyword']
        category = form.cleaned_data['category']
        results = KeywordAnalysis.objects.filter(keyword__icontains=keyword, category=category)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'results': list(results.values())})
    return render(request, 'keyword_tool/keyword_analysis.html', {'form': form, 'results': results})

def keyword_list(request):
    keywords = KeywordAnalysis.objects.all()
    return render(request, 'keyword_tool/keyword_list.html', {'keywords': keywords})

from django.shortcuts import render
from .forms import KeywordOptimizationForm

COMMON_WORDS = set(["up", "down", "the", "and", "a", "to", "in", "is", "it", "you", "that", "he", "was", "for", "on", "are", "with", "as", "I", "his", "they", "be", "at", "one", "have", "this", "from", "or", "had", "by", "not", "word", "but", "what", "some", "we", "can", "out", "other", "were", "all", "there", "when", "up", "use", "your", "how", "said", "an", "each", "she"])

def keyword_optimization(request):
    form = KeywordOptimizationForm(request.POST or None)
    optimized_keywords = None

    if form.is_valid():
        keywords = form.cleaned_data['keywords']
        remove_duplicates = form.cleaned_data['remove_duplicates']
        maintain_phrases = form.cleaned_data['maintain_phrases']
        protect_numbers = form.cleaned_data['protect_numbers']
        convert_to_lowercase = form.cleaned_data['convert_to_lowercase']
        add_comma_with_spaces = form.cleaned_data['add_comma_with_spaces']
        add_comma_without_spaces = form.cleaned_data['add_comma_without_spaces']
        include_word_frequency = form.cleaned_data['include_word_frequency']
        remove_common_words = form.cleaned_data['remove_common_words']
        remove_single_letter_words = form.cleaned_data['remove_single_letter_words']
        replace_word = form.cleaned_data['replace_word']
        replace_with = form.cleaned_data['replace_with']

        # Split keywords into a list
        keyword_list = [kw.strip() for kw in keywords.replace(',', '\n').split('\n') if kw.strip()]

        # Remove duplicates
        if remove_duplicates:
            keyword_list = list(set(keyword_list))

        # Convert to lowercase
        if convert_to_lowercase:
            keyword_list = [kw.lower() for kw in keyword_list]

        # Replace words
        if replace_word and replace_with:
            keyword_list = [kw.replace(replace_word, replace_with) for kw in keyword_list]

        # Remove common words
        if remove_common_words:
            keyword_list = [kw for kw in keyword_list if kw not in COMMON_WORDS]

        # Remove single letter words
        if remove_single_letter_words:
            keyword_list = [kw for kw in keyword_list if len(kw) > 1]

        # Protect numbers
        if protect_numbers:
            keyword_list = [kw for kw in keyword_list if not kw.isdigit()]

        # Maintain phrases (not splitting phrases into individual words)
        if maintain_phrases:
            keyword_list = [' '.join(kw.split()) for kw in keyword_list]

        # Add comma with spaces
        if add_comma_with_spaces:
            optimized_keywords = ', '.join(keyword_list)
        # Add comma without spaces
        elif add_comma_without_spaces:
            optimized_keywords = ','.join(keyword_list)
        else:
            optimized_keywords = '\n'.join(keyword_list)

        # Include word frequency count
        if include_word_frequency:
            word_frequency = {}
            for kw in keyword_list:
                word_frequency[kw] = word_frequency.get(kw, 0) + 1
            optimized_keywords += '\n\nWord Frequency:\n'
            for word, freq in word_frequency.items():
                optimized_keywords += f'{word}: {freq}\n'

    return render(request, 'keyword_tool/keyword_optimization.html', {'form': form, 'optimized_keywords': optimized_keywords})

from django.shortcuts import render

def test_login_template(request):
    return render(request, 'keyword_tool/login.html')
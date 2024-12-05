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

from django.shortcuts import render
from .forms import ReviewAnalysisForm
from textblob import TextBlob
import matplotlib.pyplot as plt
import io
import base64

def review_analysis(request):
    analysis_result = None
    polarity_scores = []
    subjectivity_scores = []
    error_message = None

    if request.method == 'POST':
        form = ReviewAnalysisForm(request.POST)
        if form.is_valid():
            asin = form.cleaned_data['asin']
            review_text = form.cleaned_data['review_text']
            reviews = []

            if asin:
                # Fetch reviews based on ASIN (placeholder implementation)
                reviews = get_reviews(asin)
                if not reviews:
                    error_message = "Incorrect ASIN. Please enter a correct ASIN."

            if review_text:
                reviews.extend([{'content': review} for review in review_text.split('.') if review.strip()])

            if reviews:
                for review in reviews:
                    analysis = TextBlob(review['content'])
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
                ax.pie([subjective_count, objective_count], labels=['Subjective', 'Objective'], autopct='%1.1f%%', startangle=90)
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
                    'reviews': zip([review['content'] for review in reviews], polarity_scores, subjectivity_scores)
                }
    else:
        form = ReviewAnalysisForm()
        
    return render(request, 'keyword_tool/review_analysis.html', {'form': form, 'analysis_result': analysis_result, 'error_message': error_message})

def get_reviews(asin):
    # Implement the logic to fetch reviews for the given ASIN
    # This is a placeholder implementation
    if asin == "valid_asin":
        return [
            {'title': 'Great product', 'content': 'I really liked this product. It works as expected.', 'rating': 5},
            {'title': 'Not bad', 'content': 'The product is okay, but could be better.', 'rating': 3},
            {'title': 'Terrible', 'content': 'I did not like this product at all.', 'rating': 1},
        ]
    else:
        return []

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

from django.shortcuts import render
from django.http import JsonResponse
from .forms import KeywordAnalysisForm
from .models import KeywordAnalysis

def keyword_analysis(request):
    form = KeywordAnalysisForm(request.GET or None)
    results = None

    if form.is_valid():
        keyword = form.cleaned_data['keyword']
        category = form.cleaned_data['category']
        results = KeywordAnalysis.objects.filter(keyword__icontains=keyword, category=category)
        print("Results:", results)  # Debugging line
        for result in results:
            print("Avg. Monthly Sales:", result.avg_monthly_sales)  # Debugging line

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'results': list(results.values('keyword', 'category', 'search_volume', 'avg_monthly_sales', 'competition', 'suggested_bid'))})
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

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CerebroForm, FetchListingForm, CreateListingForm, KeywordOptimizationForm

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

def cerebro(request):
    if request.method == 'POST':
        form = CerebroForm(request.POST)
        if form.is_valid():
            # Process the ASINs and get the keywords
            asins = form.cleaned_data['asins'].split(',')
            asins = [asin.strip() for asin in asins if asin.strip()]  # Clean up whitespace
            keywords = get_keywords(asins)  # Replace with actual function to get keywords
            return render(request, 'keyword_tool/cerebro_results.html', {'form': form, 'keywords': keywords})
    else:
        form = CerebroForm()
    return render(request, 'keyword_tool/cerebro.html', {'form': form})

def listing_maker(request):
    keywords = request.GET.get('keywords', '')
    return render(request, 'keyword_tool/listing_maker.html', {'keywords': keywords})

def fetch_listing(request):
    if request.method == 'POST':
        form = FetchListingForm(request.POST)
        if form.is_valid():
            asin = form.cleaned_data['asin']
            # Fetch the listing details using the ASIN
            listing = get_listing_by_asin(asin)  # Replace with actual function to fetch listing
            return render(request, 'keyword_tool/listing_details.html', {'listing': listing})
    elif request.method == 'GET' and 'identifier' in request.GET:
        identifier = request.GET['identifier']
        form = FetchListingForm(initial={'asin': identifier})
        return render(request, 'keyword_tool/listing_maker.html', {'form': form})
    else:
        form = FetchListingForm()
    return render(request, 'keyword_tool/listing_maker.html', {'form': form})

def create_listing(request):
    if request.method == 'POST':
        form = CreateListingForm(request.POST)
        if form.is_valid():
            # Process the form data and create a new listing
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            # Save the new listing (replace with actual save logic)
            save_listing(title, description, price)
            return redirect('listing_maker')
    else:
        form = CreateListingForm()
    return render(request, 'keyword_tool/listing_maker.html', {'form': form})

def keyword_optimization(request):
    if request.method == 'POST':
        form = KeywordOptimizationForm(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data['keywords']
            # Process the keywords (e.g., remove duplicates, maintain phrases, etc.)
            optimized_keywords = process_keywords(keywords, form.cleaned_data)
            return render(request, 'keyword_tool/keyword_optimization.html', {
                'form': form,
                'optimized_keywords': optimized_keywords
            })
    else:
        keywords = request.GET.get('keywords', '')
        form = KeywordOptimizationForm(initial={'keywords': keywords})
    return render(request, 'keyword_tool/keyword_optimization.html', {'form': form})

def process_keywords(keywords, options):
    # Implement the keyword processing logic here
    # For example, remove duplicates, maintain phrases, remove numbers, convert to lowercase, etc.
    # This is a placeholder implementation
    keyword_list = keywords.split('\n')
    if options.get('remove_duplicates'):
        keyword_list = list(set(keyword_list))
    if options.get('maintain_phrases'):
        # Implement phrase maintenance logic
        pass
    if options.get('protect_numbers'):
        keyword_list = [kw for kw in keyword_list if not any(char.isdigit() for char in kw)]
    if options.get('convert_to_lowercase'):
        keyword_list = [kw.lower() for kw in keyword_list]
    return '\n'.join(keyword_list)

def get_keywords(asins):
    # Dummy data for demonstration purposes
    keywords = [
        {'keyword': 'example1', 'sales': 100, 'volume': 1000, 'ppc_bid': 1.5, 'sponsored_asins': 10, 'competing_products': 100},
        {'keyword': 'example2', 'sales': 200, 'volume': 2000, 'ppc_bid': 2.5, 'sponsored_asins': 20, 'competing_products': 200},
        # Add more dummy data as needed
    ]
    return keywords

from django.shortcuts import render
from .forms import SalesGuesstimatorForm

def sales_guesstimator(request):
    sales_result = None
    error_message = None

    if request.method == 'POST':
        form = SalesGuesstimatorForm(request.POST)
        if form.is_valid():
            product_asin = form.cleaned_data['product_asin']
            category = form.cleaned_data['category']
            sales_result = analyze_sales(product_asin, category)
            if not sales_result:
                error_message = "No sales data found for the given input."
    else:
        form = SalesGuesstimatorForm()
        
    return render(request, 'keyword_tool/sales_guesstimator.html', {'form': form, 'sales_result': sales_result, 'error_message': error_message})

def analyze_sales(product_asin, category):
    # Implement the logic to analyze sales for the given product or category
    # This is a placeholder implementation
    if product_asin == "valid_asin" or category:
        monthly_sales = 1000  # Placeholder value
        average_price = 20  # Placeholder value for average price per unit
        estimated_revenue = monthly_sales * average_price
        return {
            'product_asin': product_asin,
            'category': category,
            'monthly_sales': monthly_sales,
            'estimated_revenue': estimated_revenue
        }
    else:
        return None
    
from django.shortcuts import render
from .forms import ListingBoosterForm

def listing_booster(request):
    analysis_result = None
    competitor_analysis_result = None
    error_message = None
    score = 0
    competitor_score = 0
    scores = None  
    competitor_scores = None

    if request.method == 'POST':
        form = ListingBoosterForm(request.POST)
        if form.is_valid():
            main_listing = form.cleaned_data['main_listing']
            competitor_listing = form.cleaned_data['competitor_listing']

            listing = fetch_listing(main_listing)
            competitor_listing_data = fetch_listing(competitor_listing)

            if not listing:
                error_message = "No listing found for the given input."
            else:
                analysis_result, score, scores = analyze_listing(listing)
                
            if competitor_listing_data:
                     competitor_analysis_result, competitor_score, competitor_scores = analyze_listing(competitor_listing_data)
    else:
        form = ListingBoosterForm()
        
    return render(request, 'keyword_tool/listing_booster.html', {
        'form': form,
        'analysis_result': analysis_result,
        'competitor_analysis_result': competitor_analysis_result,  # New variable
        'error_message': error_message,
        'score': score,
        'competitor_score': competitor_score,
        'scores': scores,
        'competitor_scores': competitor_scores
    })

def fetch_listing(identifier):
    # Implement the logic to fetch the listing based on ASIN or URL
    # This is a placeholder implementation
    if identifier == "valid_asin" or identifier.startswith("http"):
        return {
            'title': 'Sample Product Title',
            'description': 'Sample product description.',
            'price': '1000',
            'reviews': 'Sample reviews.',
            'images': ['image1.jpg', 'image2.jpg']
        }
    else:
        return None

def analyze_listing(listing):
    # Implement the AI logic to analyze the listing and show areas of improvement
    # This is a placeholder implementation
    improvements = {
        'title': {
            'title_length': [],
            'search_volume_keywords': []
        },
        'description': {
            'search_volume_keywords': [],
            'description_length': [],
            'count_of_features': []
        },
        'pricing': [],
        'images': {
            'count_of_images': [],
            'quality_of_images': []
        }
    }
    scores = {
        'title': 100,
        'description': 100,
        'pricing': 100,
        'images': 100
    }
    
    if len(listing['title']) < 50:
        improvements['title']['title_length'].append("Title is too short. Consider adding more keywords.")
        scores['title'] -= 20
    if len(listing['description']) < 200:
        improvements['description']['description_length'].append("Description is too short. Consider adding more details.")
        scores['description'] -= 20
    if int(listing['price']) > 500:
        improvements['pricing'].append("Price is too high. Consider reducing the price.")
        scores['pricing'] -= 20
    if len(listing['images']) < 5:
        improvements['images']['count_of_images'].append("Not enough images. Consider adding more images.")
        scores['images'] -= 20

    overall_score = (scores['title'] + scores['description'] + scores['pricing'] + scores['images']) / 4

    return improvements, overall_score, scores
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('keyword_forge/', views.keyword_forge, name='keyword_forge'),
    path('keyword_list/', views.keyword_list, name='keyword_list'),
    path('delete/<int:keyword_id>/', views.delete_keyword, name='delete_keyword'),
    path('edit/<int:keyword_id>/', views.edit_keyword, name='edit_keyword'),
    path('detail/<int:keyword_id>/', views.keyword_detail, name='keyword_detail'),
    path('toggle_favorite/<int:keyword_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('review_analysis/', views.review_analysis, name='review_analysis'),
    path('product_explorer/', views.product_explorer, name='product_explorer'),
    path('keycleanse/', views.keycleanse, name='keycleanse'),
    path('login/', auth_views.LoginView.as_view(template_name='keyword_tool/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('spyglass/', views.spyglass, name='spyglass'),
    path('listing_craft/', views.listing_craft, name='listing_craft'),
    path('listing_booster/', views.listing_booster, name='listing_booster'),
    path('fetch_listing/', views.fetch_listing, name='fetch_listing'),
    path('create_listing/', views.create_listing, name='create_listing'),
    path('sales_guesstimator/', views.sales_guesstimator, name='sales_guesstimator'),
    path('scrape_reviews/', views.scrape_reviews, name='scrape_reviews'),
]

handler500 = 'my_app.views.custom_server_error'
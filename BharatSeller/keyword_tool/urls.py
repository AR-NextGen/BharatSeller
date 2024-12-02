from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('keyword_analysis/', views.keyword_analysis, name='keyword_analysis'),
    path('keyword_list/', views.keyword_list, name='keyword_list'),
    path('delete/<int:keyword_id>/', views.delete_keyword, name='delete_keyword'),
    path('edit/<int:keyword_id>/', views.edit_keyword, name='edit_keyword'),
    path('detail/<int:keyword_id>/', views.keyword_detail, name='keyword_detail'),
    path('toggle_favorite/<int:keyword_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('review_analysis/', views.review_analysis, name='review_analysis'),
    path('product_search/', views.product_search, name='product_search'),
    path('keyword_optimization/', views.keyword_optimization, name='keyword_optimization'),
    path('login/', auth_views.LoginView.as_view(template_name='keyword_tool/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('cerebro/', views.cerebro, name='cerebro'),
    path('listing_maker/', views.listing_maker, name='listing_maker'),
    path('fetch_listing/', views.fetch_listing, name='fetch_listing'),
    path('create_listing/', views.create_listing, name='create_listing'),
]
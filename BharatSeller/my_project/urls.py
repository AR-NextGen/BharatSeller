from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from keyword_tool import views as keyword_tool_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('keyword_tool.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='keyword_tool/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', keyword_tool_views.register, name='register'),
    path('test-login/', keyword_tool_views.test_login_template, name='test_login_template'),
]
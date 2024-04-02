from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user'

urlpatterns = [
    #path('login/', views.custom_login, name='custom_login'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', include('deal.urls'), name='index'),
]
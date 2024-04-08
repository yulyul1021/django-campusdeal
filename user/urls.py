from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', include('deal.urls'), name='index'),
    path('myinfo/', views.myinfo, name='myinfo'),
    path('edit/', views.edit, name='edit'),
    path('password/', views.edit_pw, name='edit_pw'),
]
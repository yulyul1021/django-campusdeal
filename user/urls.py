from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import send_verification_email, activate_user

app_name = 'user'

urlpatterns = [
    path('', include('deal.urls'), name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('myinfo/', views.myinfo, name='myinfo'),
    path('<int:pk>/', views.user_info, name='user_info'),
    path('send-email/', send_verification_email, name='send_verification_email'),
    path('activate/<uidb64>/<token>/', activate_user, name='activate_user'),
]
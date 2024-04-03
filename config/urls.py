from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('deal.urls'), name='index'),
    path('chat/', include('chat.urls')),
    path('user/', include('user.urls')),
]

from django.urls import path
from . import views

app_name = 'deal'

urlpatterns = [
    path('', views.index,name='index'),
    path('deal/<int:deal_id>/', views.detail,name='deal_detail'),
    path('deal/create/',views.deal_create,name='deal_create'),
    path('deal/list/detail',views.deal_list_detail,name='deal_list_detail'),
    path('deal/edit/<int:deal_id>/',views.deal_edit,name='deal_edit'),
    path('deal/delete/<int:deal_id>/',views.deal_delete,name='deal_delete'),
]


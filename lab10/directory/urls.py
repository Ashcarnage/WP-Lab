from django.urls import path
from . import views

app_name = 'directory'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('page/<int:page_id>/', views.view_page, name='view_page'),
    path('like_page/<int:page_id>/', views.like_page, name='like_page'),
    path('like_category/<slug:category_name_slug>/', views.like_category, name='like_category'),
]
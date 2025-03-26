from django.urls import path
from . import views

urlpatterns = [
    path('form/', views.rating_form, name='rating_form'),
    path('vote/', views.submit_vote, name='submit_vote'),
    path('reset/', views.reset_vote, name='reset_vote')
]

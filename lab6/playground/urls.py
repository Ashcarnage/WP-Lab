from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calculator/',views.calculator_view),
    path('magazine/',views.magazine_cover)
]

from django.urls import path
from . import views
from .views import car_form_view, car_result_view

urlpatterns = [
    path('',car_form_view,name='car_form'),
    path('result/',car_result_view,name='car_result'),
    path('hello/',views.home,name="home")
]
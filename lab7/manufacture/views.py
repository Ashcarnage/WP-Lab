from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CarForm
# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, Django!")

def car_form_view(request):
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            # Retrieve cleaned data from form fields
            manufacturer = form.cleaned_data['manufacturer']
            model_name = form.cleaned_data['model_name']
            # Forward to result view with parameters via query string
            return redirect(reverse('car_result') + 
                            f'?manufacturer={manufacturer}&model_name={model_name}')
    else:
        form = CarForm()
    return render(request, 'car_form.html', {'form': form})

def car_result_view(request):
    # Retrieve parameters from the URL's query string
    manufacturer = request.GET.get('manufacturer', 'Not Selected')
    model_name = request.GET.get('model_name', 'Not Provided')
    context = {
        'manufacturer': manufacturer,
        'model_name': model_name,
    }
    return render(request, 'car_result.html', context)
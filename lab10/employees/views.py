# employees/views.py
from django.shortcuts import render, redirect
from django.db import connection
from .models import Works, Lives
from .forms import WorksForm, CompanySearchForm

def index(request):
    works_form = WorksForm()
    search_form = CompanySearchForm()
    
    if request.method == 'POST':
        if 'add_works' in request.POST:
            works_form = WorksForm(request.POST)
            if works_form.is_valid():
                works_form.save()
                return redirect('index')
                
    context = {
        'works_form': works_form,
        'search_form': search_form,
    }
    return render(request, 'employees/index.html', context)

def search_company(request):
    search_form = CompanySearchForm()
    results = []
    
    if request.method == 'POST':
        search_form = CompanySearchForm(request.POST)
        if search_form.is_valid():
            company_name = search_form.cleaned_data['company_name']
            
            # Using raw SQL query to join the tables
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT w.person_name, w.salary
                    FROM employees_works w
                    LEFT JOIN employees_lives l ON w.person_name = l.person_name
                    WHERE w.company_name = %s
                """, [company_name])
                results = cursor.fetchall()
    
    context = {
        'search_form': search_form,
        'results': results,
        'works_form': WorksForm(),
    }
    return render(request, 'employees/index.html', context)

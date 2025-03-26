# directory/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from .models import Category, Page
from .forms import CategoryForm, PageForm
from django.contrib.auth.decorators import login_required

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {
        'categories': category_list,
        'pages': page_list
    }
    
    return render(request, 'directory/index.html', context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    
    try:
        category = Category.objects.get(slug=category_name_slug)
        
        # Increment the visits counter
        category.visits += 1
        category.save()
        
        pages = Page.objects.filter(category=category)
        
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    
    return render(request, 'directory/category.html', context_dict)

def view_page(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    
    # Increment the views counter
    page.views += 1
    page.save()
    
    # Check if user has liked the page
    is_liked = False
    if request.user.is_authenticated:
        if page.likes.filter(id=request.user.id).exists():
            is_liked = True
    
    return render(request, 'directory/page.html', {
        'page': page,
        'is_liked': is_liked,
        'total_likes': page.number_of_likes()
    })

@login_required
def like_page(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    
    if page.likes.filter(id=request.user.id).exists():
        # User already liked this page, so remove the like
        page.likes.remove(request.user)
    else:
        # User hasn't liked this page yet, so add the like
        page.likes.add(request.user)
    
    return redirect('directory:view_page', page_id=page.id)

@login_required
def like_category(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)
    
    # Simple increment for category likes
    category.likes += 1
    category.save()
    
    return redirect('directory:show_category', category_name_slug=category.slug)

def add_category(request):
    form = CategoryForm()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('directory:index')
    
    return render(request, 'directory/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect('directory:show_category', category_name_slug=category_name_slug)
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'directory/add_page.html', context_dict)

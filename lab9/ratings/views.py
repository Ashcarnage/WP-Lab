from django.shortcuts import render, redirect
from .models import BookRating

def rating_form(request):
    percentages = BookRating.get_percentages()
    voted = request.session.get('has_voted', False)
    
    # Get total votes count
    total_votes = BookRating.objects.count()
    
    return render(request, 'ratings/rating_form.html', {
        'percentages': percentages,
        'voted': voted,
        'total_votes': total_votes
    })

def submit_vote(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        if rating in ['good', 'satisfactory', 'bad']:
            BookRating.objects.create(rating=rating)
            request.session['has_voted'] = True
    
    return redirect('rating_form')

def reset_vote(request):
    if 'has_voted' in request.session:
        del request.session['has_voted']
    return redirect('rating_form')



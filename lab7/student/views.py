from django.shortcuts import render,redirect

def first_page(request):
    if request.method == 'POST':
        # Retrieve data from the form
        name = request.POST.get('Name')
        roll = request.POST.get('Roll')
        subject = request.POST.get('Subjects')
        
        # Save data in the session
        request.session['name'] = name
        request.session['roll'] = roll
        request.session['subject'] = subject
        
        # Redirect to second page
        return redirect('second_page')
    
    # Render firstPage.html on GET request
    return render(request, 'firstPage.html')


def second_page(request):
    if request.method == 'POST':
        # The button click on second page navigates back to the first page.
        return redirect('first_page')
    
    # Retrieve data stored in session
    name = request.session.get('name', '')
    roll = request.session.get('roll', '')
    subject = request.session.get('subject', '')
    message = f"Name: {name}, Roll: {roll}, Subject: {subject}"
    
    # Pass the message to the template context
    context = {'msg': message}
    return render(request, 'secondPage.html', context)

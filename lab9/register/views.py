from django.shortcuts import render, redirect
from .forms import RegistrationForm

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Get form data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            contact_number = form.cleaned_data['contact_number']
            
            # Store data in session
            request.session['user_data'] = {
                'username': username,
                'email': email,
                'contact_number': contact_number
            }
            
            # Debug print to check if this code is reached
            print("Form is valid, redirecting to success page")
            
            return redirect('success')
        else:
            # Debug print to see form errors
            print(f"Form errors: {form.errors}")
    else:
        form = RegistrationForm()
    
    return render(request, 'register/register.html', {'form': form})
def success_view(request):
    # Get user data from session
    user_data = request.session.get('user_data', {})
    
    # Debug print
    print(f"Success view accessed with user data: {user_data}")
    
    return render(request, 'register/success.html', {'user_data': user_data})

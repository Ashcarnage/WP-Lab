
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, Django!")

def calculator_view(request):
    result = None
    error = None
    if request.method == "POST":
        try:
            num1 = int(request.POST.get('num1', ''))
            num2 = int(request.POST.get('num2', ''))
            operation = request.POST.get('operation')
            
            if operation == "add":
                result = num1 + num2
            elif operation == "subtract":
                result = num1 - num2
            elif operation == "multiply":
                result = num1 * num2
            elif operation == "divide":
                if num2 == 0:
                    error = "Cannot divide by zero."
                else:
                    result = num1 / num2
            else:
                error = "Invalid operation selected."
        except (TypeError, ValueError):
            error = "Please provide valid integer inputs."
            
    context = {
        'result': result,
        'error': error
    }
    return render(request, 'cal.html', context)


from django.shortcuts import render

def magazine_cover(request):
    cover = {}
    if request.method == "POST":
        # Retrieve form data with default values if not provided
        cover['image'] = request.POST.get('image', '')
        cover['bg_color'] = request.POST.get('background_color', '#ffffff')
        cover['message'] = request.POST.get('message', 'Your Magazine Title')
        cover['text_color'] = request.POST.get('text_color', '#000000')
        cover['font_size'] = request.POST.get('font_size', '50')
        cover['font_family'] = request.POST.get('font_family', 'Arial, sans-serif')
    return render(request, 'magazine_cover.html', {'cover': cover})

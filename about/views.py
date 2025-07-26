from django.shortcuts import render

def about(request):
    return render(request, 'about.html')

def liderplatform1(request):
    return render(request, 'glavfooter/liderplatform.html')
    
def workshop1(request):
    return render(request, 'glavfooter/workshop.html')

def documents1(request):
    return render(request, 'glavfooter/documents.html')

def shop1(request):
    return render(request, 'glavfooter/shop.html')

def service1(request):
    return render(request, 'glavfooter/service.html')

def contact1(request):
    return render(request, 'glavfooter/contact.html')
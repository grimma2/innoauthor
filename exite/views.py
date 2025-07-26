from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect


def exite(request):
    return render(request, 'exite.html')

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

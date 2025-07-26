from django.urls import path
from . import views

app_name = "about"
urlpatterns = [
    path('', views.about, name='about'),
    path('liderplatform1/', views.liderplatform1, name='liderplatform1'),
    path('workshop1/', views.workshop1, name='workshop1'),
    path('documents1/', views.documents1, name='documents1'),
    path('shop1/', views.shop1, name='shop1'),
    path('service1/', views.service1, name='service1'),
    path('contact1/', views.contact1, name='contact1'),
]
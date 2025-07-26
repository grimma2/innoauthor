from django.urls import path
from . import views

app_name = "startpage"
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('vhod/', views.vhod, name='vhod'),
    path('liderplatform/', views.liderplatform, name='liderplatform'),
    path('workshop/', views.workshop, name='workshop'),
    path('documents/', views.documents, name='documents'),
    path('shop/', views.shop, name='shop'),
    path('service/', views.service, name='service'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('cookie/', views.cookie, name='cookie'),
    path('soglasie/', views.soglasie, name='soglasie'),
]
from django.urls import path
from phishing import views

urlpatterns = [
    path('nhan/', views.home_view, name='home_view'),
    path('', views.predict_phishing_link, name='predict_phishing_link'),
]
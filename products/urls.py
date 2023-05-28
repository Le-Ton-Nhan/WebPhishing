from django.urls import path

from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('myurl', views.MyUrl, name='MyUrl'),
    path('viewurl/<str:pid>/', views.url_details, name='url_details'),
]

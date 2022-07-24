''' Url mapping for home module '''
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('authorise', views.authorise, name='authorise'),
]

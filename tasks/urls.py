''' Url mapping for tasks web app '''
from django.urls import path

from . import views

urlpatterns = [
    path('holding_page', views.holding_page, name='holding_page'),
]

''' Views for main app '''
from django.shortcuts import render


# Create your views here.
def index(request):
    ''' Holding Page'''
    return render(request, 'main/index.html')

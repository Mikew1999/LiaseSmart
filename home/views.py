''' Home page handling '''
from django.shortcuts import render
# Create your views here.


def index(request):
    ''' home page '''
    # Site tracking
    return render(request, 'home/index.html')

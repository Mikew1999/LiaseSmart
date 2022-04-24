from django.shortcuts import render
# Create your views here.


def index(request):
    ''' Testing '''
    return render(request, 'home/index.html')

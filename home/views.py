''' Home page handling '''
from datetime import date, datetime, timedelta
from django.shortcuts import render
from .models import SiteActionsTaken, SiteVisits, SiteErrors


def find_ip(request):
    ''' Finds IP address of user '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_addr = x_forwarded_for.split(',')[-1].strip()
    else:
        ip_addr = request.META.get('REMOTE_ADDR')
    return ip_addr


def index(request):
    ''' home page '''
    # Site tracking
    today = date.today()
    ip_addresses = SiteVisits.objects.all()
    users_ip = find_ip(request)
    print(users_ip)

    if users_ip not in ip_addresses:
        SiteVisits(date=today, site_visits='')

    return render(request, 'home/index.html')

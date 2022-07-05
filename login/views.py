''' Login page and login form handling '''
from django.shortcuts import render
from tasks.bg_processes.login import login


# Create your views here.
def login_page(request):
    '''
        Renders login page, handles
        login form, cleans data from form
    '''
    user_type = request.GET.get("user_type", None)

    if request.method == 'POST':
        # csrf_token = request.POST['csrf_token']
        username = str(request.POST['username'])
        password = str(request.POST['password'])

        form = {
            'username': username,
            'password': password
        }

        check_login = login(form)

        return check_login

    if user_type == '1':
        return render(request, 'login/artist_login.html')
    elif user_type == '2':
        return render(request, 'login/liaison_login.html')
    else:
        return render(request, 'login/login_select.html')

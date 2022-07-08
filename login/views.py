''' Login page and login form handling '''
from django.shortcuts import render, redirect
from django.contrib import messages
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

        # calls login function to clean data and
        # check for user
        check_login = login(form=form)

        # if user found
        if check_login:
            # if users account has been deleted
            # redirect to signup page
            if check_login['deleted'] == '1':
                messages.add_message(
                    request, messages.INFO,
                    'Your account is no longer active, please sign up')
                # add sign up redirect here
                return

            # if users account is active
            if check_login['active'] == '1':
                # if account is not locked and is active
                # redirect to dash home page
                if check_login['locked'] != '1':
                    # put redirect to check two fa function here
                    context = check_login
                    return context
                # if users account is locked
                # redirect to login page and show message
                else:
                    locked_until = check_login['locked_until']
                    messages.add_message(
                        request, messages.INFO,
                        'Your account is temporarily locked'
                        f'please try again in {locked_until}')
                    return render(request, 'login/artist_login.html')
            # if users account is not authorised then
            # redirect to authorise page
            else:
                context = check_login
                # put redirect to authorise login page here
                return redirect(request, authorise(request, context=context))
        # if user not found / incorrect username or password
        else:
            # add redirect to relevant login page
            messages.add_message(request, messages.WARNING,
                                 'Incorrect username or password')
            return render(request, 'login/artist_login.html')

    if user_type == '1':
        return render(request, 'login/artist_login.html')
    elif user_type == '2':
        return render(request, 'login/liaison_login.html')
    else:
        return render(request, 'login/login_select.html')


def authorise(request, context):
    ''' Authorise account page '''
    return render(request, 'login/authorise.html', context)

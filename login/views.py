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

        # if error
        if check_login['error']:
            the_error = check_login['error']
            if the_error == 'locked':
                locked_until = check_login['locked_until']
                messages.add_message(
                    request, messages.ERROR,
                    f'Account locked until {locked_until}'
                )
                # redirect to login page
            elif the_error == 'account not active':
                messages.add_message(
                    request, messages.INFO,
                    'Account has not yet been activated.'
                    'Please activate your account'
                )
                # add redirect to activate page
                return
            elif the_error == 'incorrect login':
                if check_login['attempt']:
                    attempt = check_login['attempt']
                    messages.add_message(
                        request, messages.ERROR,
                        f'Incorrect login details. Attempt: {attempt}'
                    )
                    # add redirect to login page and add message
            else:
                messages.add_message(
                    request, messages.ERROR,
                    'Something went wrong. Please try again later'
                )
                # add redirect to login page

        # if no error redirect to dash function
        else:
            user_details = check_login['user_details']
            messages.add_message(
                request, messages.SUCCESS,
                f'Hello! {user_details["username"]}'
            )
            # add redirect to dash page
            return

    return render(request, 'login/login.html')


def authorise(request, context):
    ''' Authorise account page '''
    return render(request, 'login/authorise.html', context)

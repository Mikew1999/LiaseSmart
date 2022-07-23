''' Login page and login form handling '''
from django.shortcuts import render, redirect
from django.contrib import messages
from tasks.bg_processes.login import login


# Login page and functionality
def login_page(request):
    '''
        Renders login page, handles
        login form, cleans data from form
    '''

    if request.method == 'POST':
        # csrf_token = request.POST['csrf_token']
        username = request.POST['username']
        password = request.POST['password']

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

            # if account is locked
            if the_error == 'locked':
                locked_until = check_login['locked_until']
                messages.add_message(
                    request, messages.ERROR,
                    f'Account locked until {locked_until}'
                )

                # render login page and show message
                return render(request, 'login/login.html')

            # if account not active
            elif the_error == 'account not active':
                messages.add_message(
                    request, messages.INFO,
                    'Account has not yet been activated.'
                    'Please activate your account'
                )

                context = check_login['user_details']

                # redirect to authorise page
                return redirect(authorise, context=context)

            # if login details are incorrect
            elif the_error == 'incorrect login':
                if check_login['attempt']:
                    attempt = check_login['attempt']
                    messages.add_message(
                        request, messages.ERROR,
                        f'Incorrect login details. Attempt: {attempt}'
                    )
                    # render login page and show message
                    return render(request, 'login/login.html')

            # any sql errors
            else:
                messages.add_message(
                    request, messages.ERROR,
                    'Something went wrong. Please try again later'
                )
                # render login page and show message
                return render(request, 'login/login.html')

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


# activate account page and functionality
def authorise(request, context):
    ''' Activate account page '''
    if request.method == 'POST':

        if request.POST['authcode']:
            if request.POST['authcode'] == context['activation_code']:
                messages.add_message(
                    request, messages.SUCCESS,
                    'Account activated!'
                )
                return
            else:
                messages.add_message(
                    request, messages.ERROR,
                    'Activation code incorrect'
                )
                return render(request, 'login/authorise.html', context=context)

        if request.POST['newcode']:
            sender_email = 'liaisesmartsupport@gmail.com'
            receiver_email = context['email_addr']
            # create random passcode
            
            email_content = f'Activation code: {activation_code}'
    return render(request, 'login/authorise.html', context=context)

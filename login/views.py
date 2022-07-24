''' Login page and login form handling '''
import random
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from tasks.bg_processes.login import login
from tasks.bg_processes.send_email import send_email
from tasks.bg_processes.acitvate_account import activate_account


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

                user_id = check_login['user_details']['user_id']
                activation_key = check_login['user_details']['activation_key']
                activation_expiry = check_login['user_details']['activation_expiry']

                context = {
                    'user_id': user_id,
                    'activation_code': activation_key,
                    'activation_expiry': activation_expiry,

                }

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
def authorise(request, context=None):
    ''' Activate account page '''
    current_date_time = datetime.now()

    if context is None:
        context = {
            'activation_code': request.get('activation_code', None),
            'activation_expiry': request.get('activation_expiry', None),
            'user_id': request.get('user_id', None)
        }
        for key, value in context:
            if context['key'] is None:
                # redirect to error page
                return

    # if form submitted
    if request.method == 'POST':

        # if user has submitted acitvation code
        if request.POST['authcode']:
            # if activation code entered matches
            # activation code in db
            if request.POST['authcode'] == context['activation_code']:
                # if activation code hasn't expired
                if current_date_time <= context['activation_expiry']:
                    # add success message and redirect to dash page / setup

                    account_active = activate_account(context=context)

                    if account_active == 1:
                        messages.add_message(
                            request, messages.SUCCESS,
                            'Account activated!'
                        )
                        return  # add redirect to check dash func
                    else:
                        messages.add_message(
                            request, messages.ERROR,
                            'Something went wrong. Please try again.'
                        )
                        # redirect to authorise page with context passed in
                # if activation code has expired
                else:
                    messages.add_message(
                        request, messages.ERROR,
                        'Account activation code expired, please request a new code.'
                    )
                    return render(request, 'login/authorise.html',
                                  context=context)
            # if activation code doesn't match
            else:
                # add error message
                messages.add_message(
                    request, messages.ERROR,
                    'Activation code incorrect. Please try again / request another code'
                )
                # redirect to authorise page
                return render(request, 'login/authorise.html',
                              context=context)

        # if user has requested a new code
        if request.POST['newcode']:
            # email addresses
            sender_email = 'liaisesmartsupport@gmail.com'
            receiver_email = context['email_addr']
            # create random passcode to be activation code
            chars = ("abcdefghijklmnopqrstuvwxyz"
                     "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789!@#$%^&*()")
            pass_length = 16
            activation_code = ''

            # loop to build random passcode from
            # characters above
            for x in range(0, pass_length):
                activation_char = random.choice(chars)
                activation_code = activation_code + activation_char

            # sets expiry date to 2 days in the future
            new_expiry = current_date_time + timedelta(days=2)

            email_content = f'Activation code: {activation_code}'
            email_context = {
                'sender_email': sender_email,
                'receiver_email': receiver_email,
                'email_content': email_content,
                'activation_code': activation_code
            }

            send_the_email = send_email(email_context=email_context)

            if send_the_email == 'yes':
                messages.add_message(
                    request, messages.SUCCESS,
                    'Activation code sent successfully!'
                )

            else:
                messages.add_message(
                    request, messages.ERROR,
                    'Problem sending activation code. Please try again later'
                )

    if context == None:

    return render(request, 'login/authorise.html', context=context)

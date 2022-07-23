''' Sends email '''
import smtplib
import ssl
import os


def send_email(email_context):
    ''' Connects to smtp server and sends email '''
    sender_email = email_context['sender_email']
    receiver_email = email_context['to_email']
    email_content = email_context['email_content']

    try:
        message = f'Hi There /n {email_content}'
        port = 465  # For SSL
        password = os.environ.get('email_pw')

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com",
                              port, context=context) as server:
            server.login("liaisesmartsupport@gmail.com", password)
            server.sendmail(sender_email, receiver_email, message)

        sent_status = 200

    except smtplib.SMTPConnectError as err:
        print(f'Something went wrong {err}')

    return sent_status

from django.core.mail import BadHeaderError
from templated_mail.mail import BaseEmailMessage
from celery import shared_task


@shared_task
def send_verification_email(code):
    print("Sending verification email ...")
    try:
        email = BaseEmailMessage(template_name='emails/verification_email.html', context={'verification_code': code})
        email.send(['amirmemool2@gmail.com'])
    except BadHeaderError as e:
        print(f'Bad header exception occur {e}')
    print("Email Send Successfully")

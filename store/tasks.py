from celery import shared_task
from django.core.mail import BadHeaderError
from django.db.models import Count
from templated_mail.mail import BaseEmailMessage

from store.models import Cart


@shared_task
def send_verification_email(code):
    print("Sending verification email ...")
    try:
        email = BaseEmailMessage(template_name='emails/verification_email.html', context={'verification_code': code})
        email.send(['amirmemool2@gmail.com'])
    except BadHeaderError as e:
        print(f'Bad header exception occur {e}')
    print("Email Send Successfully")


@shared_task
def remove_empty_cart():
    print('Removing empty cart ...')
    Cart.objects.annotate(item_count=Count('items')).filter(item_count=0).delete()
    print('Empty Cart Removed successfully')
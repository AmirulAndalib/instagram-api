""" Background tasks module for users """

# Django imports
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Pillow imports
from PIL import Image

# Instagram tasks
from instagram.tasks import celery
# Instagram models
from instagram.core.models import User
# Instagram utils
from instagram.utils.token import generate_user_token


@celery.task(max_retries=4)
def send_verification_email(user_id):
    """ Celery task that helps to send an email verification """
    user = User.objects.get(pk=user_id)

    account_verification_token = generate_user_token(
        user = user,
        exp_mins = 15,
        token_type = 'verification_email'
    )

    subject: str = 'Account verification'
    template = render_to_string(
        template_name='emails/account_verification.html',
        context={
            'user': user,
            'token': account_verification_token,
        }
    )
    from_email: str = settings.DEFAULT_FROM_EMAIL

    msg = EmailMultiAlternatives(subject, template, from_email, to=[user.email])
    msg.attach_alternative(template, 'text/html')
    msg.send(fail_silently=False)


@celery.task
def resize_profile_pic():
    pass
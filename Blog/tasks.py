import json
from celery import shared_task
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from django.core.exceptions import ValidationError


@shared_task(bind=True)
def send_subscription_email(self, user_celery, category_celery, current_site):
    
    link = reverse('home')
    url = "http://"+current_site+link
    
    user = json.loads(user_celery)
    category = json.loads(category_celery) 
    
    body = f"Dear {user['username']},\nYou have just followed the category {category['title']} on the BLOG.\nThank you very much and have a nice time at our blog.\n click the link to go to our blog\n\n"
    message = body + url
    
    try:
        send_mail(
            subject='Category Subscription notification',
            message= message,
            from_email="settings.EMAIL_HOST_USER",
            recipient_list=[user['email'],],
            fail_silently=False
        )
    except Exception:
        raise ValidationError("Couldn't send the message to the email ! ")
    return 'Done!'
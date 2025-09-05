from celery import shared_task
from django.contrib.auth import get_user_model
User = get_user_model()

@shared_task
def send_welcome_email(user_id):
    try:
        user = User.objects.get(id=user_id)
        print(f"Sending welcome email to {user.email}")
        return True
    except User.DoesNotExist:
        return False

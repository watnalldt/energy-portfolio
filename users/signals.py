from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

# from .models import ClientManager

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def notify_admin(sender, created, instance, **kwargs):
    if not created and instance.role == "CLIENT_MANAGER":
        subject = "New Registration created"
        message = "A new client manager  %s has registered with the site" % instance.email
        from_addr = "support@energyportfolio.co.uk"
        recipient_list = (
            "jessica@energyportfolio.co.uk",
            "josh@energyportfolio.co.uk",
            "chris@energyportfolio.co.uk",
        )
        send_mail(subject, message, from_addr, recipient_list)

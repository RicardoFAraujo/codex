from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """Handle user post-save actions"""
    if created:
        # Award welcome badge or perform initial setup
        instance.check_and_award_badges()
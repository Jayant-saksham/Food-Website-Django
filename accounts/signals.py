"""
    As soon as User is created, we wish to create a UserProfile. This can be done using signals.
    Signals are used to perform any action on modification of a model instance. 
    The signals are utilities that help us to connect events with actions.
    There are 3 types of signal.

    -   pre_save/post_save: This signal  works before/after the method save().
    -   pre_delete/post_delete: This signal  works before after delete a model’s instance (method delete()) this signal is thrown.
    -   pre_init/post_init: This signal is thrown before/after instantiating a model (__init__() method).


    For using signals in Django, we need to go to other resources as Django docs and github 
    does not provide information in simple language.
    I suggest you to use GFG or StackOverflow for basics. 
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(post_save, sender=User)
def post_save_receiver(sender, instance, created, **kwargs):
    """
        -   receiver -  The function who receives the signal and does something.
        -   sender -    Sends the signal
        -   created -   Checks whether the model is created or not
        -   instance -  created model instance
        -   **kwargs -  wildcard keyword arguments

    """
    # Save() function is called and new model is created
    if created:
        UserProfile.objects.create(user=instance)

    # Save() function is called and model is updated
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)

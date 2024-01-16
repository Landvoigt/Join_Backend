import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Topic(models.Model):
    title = models.CharField(max_length=30)
    date = models.DateField(default=datetime.date.today)
    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

class Task(models.Model):
    category = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    date = models.DateField(default=datetime.date.today)
    topic = models.ForeignKey(
        Topic, 
        on_delete=models.CASCADE, 
        related_name='chat_message_set', 
        default=None,
        blank=True, 
        null=True
    )
    subtasks = models.TextField()
    prio = models.CharField(max_length=30)
    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    assigned_clients = models.ManyToManyField(
        User, 
        related_name='tasks',
        blank=True,
    )


@receiver(pre_delete, sender=User)
def remove_user_tasks(sender, instance, **kwargs):
    # Remove the user from all tasks when the user is deleted
    Task.objects.filter(assigned_clients=instance).delete()
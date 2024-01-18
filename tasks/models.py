import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from contacts.models import Contact

class Topic(models.Model):
    title = models.CharField(max_length=30, blank=True, null=True)
    color = models.CharField(max_length=15, blank=True, null=True) 
    date = models.DateField(default=datetime.date.today)
    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

class Task(models.Model):
    category = models.CharField(max_length=30, blank=True, null=True)
    title = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateField(default=datetime.date.today)
    topic = models.ForeignKey(
        Topic, 
        on_delete=models.CASCADE, 
        related_name='topics',
        default=None,
        blank=True, 
        null=True
    )
    subtasks = JSONField(blank=True, null=True)
    prio = models.CharField(max_length=30, blank=True, null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    assigned_clients = models.ManyToManyField(
        Contact, 
        related_name='tasks',
        blank=True,
    )


@receiver(pre_delete, sender=Contact)
def remove_user_tasks(sender, instance, **kwargs):
    Task.objects.filter(assigned_clients=instance).delete()
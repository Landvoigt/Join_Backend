from django.db import models

class Contact(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    initials = models.CharField(max_length=5)
    email = models.CharField(max_length=40)
    phone = models.CharField(max_length=15)
    color = models.CharField(max_length=15)
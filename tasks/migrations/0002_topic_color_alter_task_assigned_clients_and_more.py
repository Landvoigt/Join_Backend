# Generated by Django 5.0.1 on 2024-01-18 10:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_alter_contact_color_alter_contact_email_and_more'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='color',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_clients',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='contacts.contact'),
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='prio',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='subtasks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='topic',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='tasks.topic'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='title',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]

# Generated by Django 5.0.1 on 2024-01-16 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_topic_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='color',
            field=models.CharField(default=None, max_length=15),
        ),
    ]

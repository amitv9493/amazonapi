# Generated by Django 4.2.5 on 2023-09-05 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_amazon_authorization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='amazon_authorization',
        ),
    ]

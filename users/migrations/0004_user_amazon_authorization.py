# Generated by Django 4.2.5 on 2023-09-05 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_amazon_authorization'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='amazon_authorization',
            field=models.BooleanField(default=False),
        ),
    ]

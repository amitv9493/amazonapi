from django.db import models

# Create your models here.
from django.conf import settings


class user_credentials(models.Model):
    class market_place(models.TextChoices):
        Belgium = "AMEN7PMS3EDWL"
        Netherlands = "A1805IZSGTT6HS"
        Germany = "A1PA6795UKMFR9"
        Italy = "APJ6JRA9NG5V4"
        Sweden = "A2NODRKZP88ZB9"
        India = "A21TJRUUN4KGV"
        United_Kingdom = "A1F83G8C2ARO7P"
        sandbox = "ATVPDKIKX0DER"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cred")
    code = models.CharField(max_length=255, null=True)
    selling_partner_id = models.CharField(max_length=255, null=True)

    access_token = models.TextField(null=True)
    refresh_token = models.TextField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    market_place_id = models.CharField(
        max_length=255,
        null=True,
        choices=market_place.choices,
        default=market_place.sandbox,
    )

    def __str__(self):
        return str(self.user.username)

    def valid_token(self):
        import datetime

        if self.updated_at + datetime.timedelta(seconds=3600) < datetime.datetime.now():
            return False
        else:
            return True
    
    
    class Meta:
        verbose_name_plural = "User Credentials"
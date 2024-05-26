from django.db import models


# Create your models here.


class UserDetails(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    licence = models.EmailField(max_length=100)
    dni_nie = models.CharField(max_length=100)
    expedition_date = models.CharField(max_length=100)
    expiration_date = models.CharField(max_length=100)
    graduated_in = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/raw_images/', null=True, blank=True)
    card = models.ImageField(upload_to='images/cards/', null=True, blank=True)
    message_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

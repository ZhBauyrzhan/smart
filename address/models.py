from django.db import models


class Address(models.Model):
    street = models.CharField(max_length=100)
    apartment = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

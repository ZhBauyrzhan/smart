import json

from django.db import models
from django.utils.translation import gettext_lazy as _
from address.models import Address


class MeasurementUnitChoices(models.TextChoices):
    INCHES = {'in', 'Inches'}
    CENTIMETERS = {'cm', 'Centimeters'}
    POUNDS = {'lb', 'Pounds'}
    KILOGRAMS = {'kg', 'Kilograms'}
    PERCENTAGE = {'%', 'Percent'}
    TIME = {'sec', 'min', 'hours'}
    TEMPERATURE = {'kelvin'}


class PhysicalQuantityChoices(models.TextChoices):
    TEMPERATURE = {'temperature'}
    PRESSURE = {'pressure'}
    FREQUENCY = {'frequency'}
    CURRENT = {'current'}
    HUMIDITY = {'humidity'}


class Sensor(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    addresses = models.ForeignKey(to=Address, related_name='addresses', on_delete=models.PROTECT)
    ip = models.GenericIPAddressField()
    port = models.DecimalField(max_digits=4, decimal_places=0)


class Measurement(models.Model):
    sensor = models.ForeignKey(to=Sensor, verbose_name=_('Sensor to connect'), on_delete=models.CASCADE,
                               related_name='sensors')
    data=models.JSONField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    # value = models.CharField(max_length=100, verbose_name=_('Value'))
    # unit = models.CharField(max_length=100, verbose_name=_('Measurement Unit'), choices=MeasurementUnitChoices.choices)
    # physical_quantity = models.CharField(max_length=60, verbose_name=_('Physical quantity'),
    #                                      choices=PhysicalQuantityChoices.choices)
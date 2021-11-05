from django.db import models


class City(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    date = models.DateField()
    average_temperature = models.FloatField(blank=True, null=True)
    average_temperature_uncertainty = models.FloatField(blank=True, null=True)
    city = models.CharField(max_length=163)
    country = models.CharField(max_length=56)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)

    class Meta:
        db_table = "global_land_temperatures_by_city"
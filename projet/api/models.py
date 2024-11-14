from django.db import models

class AirportData(models.Model):
    start = models.CharField(max_length=255)
    temperature_en_chiffre = models.FloatField()
    humidity_en_chiffre = models.IntegerField()
    temperature_en_chiffre_2days_left = models.FloatField()
    humidity_en_chiffre_2days_left = models.IntegerField()
    faa_designator = models.CharField(max_length=10, blank=True, null=True)
    length_ft = models.FloatField(blank=True, null=True)
    tail_height_at_oew_ft = models.FloatField(blank=True, null=True)
    wheelbase_ft = models.FloatField(blank=True, null=True)
    date = models.DateField()
    std = models.TimeField()
    atd = models.TimeField(blank=True, null=True)
    type = models.CharField(max_length=50)
    fluid = models.IntegerField()
    water = models.IntegerField()
    meteo = models.CharField(max_length=50, blank=True, null=True)
    oat = models.FloatField()
    finish = models.CharField(max_length=255)
    duration = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.start} - {self.date}"


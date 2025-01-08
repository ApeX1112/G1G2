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
    std = models.FloatField()
    atd = models.TimeField(blank=True, null=True)
    type = models.CharField(max_length=50)
    fluid = models.IntegerField()
    water = models.IntegerField()
    meteo = models.CharField(max_length=50, blank=True, null=True)
    oat = models.FloatField()
    finish = models.CharField(max_length=255)
    duration = models.FloatField(blank=True, null=True)

    Wingspan_ft_without_winglets_sharklets=models.FloatField(blank=True, null=True)
    Wingspan_ft_with_winglets_sharklets=models.FloatField(blank=True, null=True)
    Cockpit_to_Main_Gear_ft=models.FloatField(blank=True, null=True)
    Main_Gear_Width_ft=models.FloatField(blank=True, null=True)
    OneStep_Fluid=models.FloatField(blank=True, null=True)
    TwoStep_I_Fluid=models.FloatField(blank=True, null=True)
    TwoStep_II_Fluid=models.FloatField(blank=True, null=True)
    deicing_time_minutes=models.FloatField(blank=True, null=True)
    meteo_numerical=models.FloatField(blank=True, null=True)
    Month=models.FloatField(blank=True, null=True)
    Year=models.FloatField(blank=True, null=True)
    ACMARK=models.CharField(max_length=255, null=True)
    ACTYPE=models.CharField(max_length=255, null=True)
    FLIGHT=models.CharField(max_length=255, null=True)
    CARRIER=models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.start} - {self.date}"


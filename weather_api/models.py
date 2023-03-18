from django.db import models

class Weather(models.Model):
    station_id = models.CharField(max_length=11)
    date = models.DateField()
    maximum_temperature = models.IntegerField()
    minimum_temperature = models.IntegerField()
    amount_of_precipitation = models.IntegerField(help_text="Unit in mm")


    class Meta:
        unique_together = ('station_id', 'date')

    def __str__(self) -> str:
        return f"{self.station_id} -> {self.date.strftime('%Y%m%d')}"
    

class WeatherStats(models.Model):
    station_id = models.CharField(max_length=11)
    year = models.CharField(max_length=4)
    average_maximum_temperature = models.FloatField()
    average_minimum_temperature = models.FloatField()
    average_amount_of_precipitation = models.FloatField(help_text="Unit in cm")

    def __str__(self) -> str:
        return f"{self.station_id} -> {self.year}"

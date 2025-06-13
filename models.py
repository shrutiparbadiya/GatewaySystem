from django.db import models

class Vehicle(models.Model):
    owner_name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=10, choices=[("Car", "Car"), ("Activa", "Activa")])
    number_plate = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.owner_name} - {self.number_plate}"

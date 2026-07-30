from django.contrib.auth.models import User
from django.db import models

class EmergencyContact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=True, blank=True)
    place = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class SOSAlert(models.Model):
    message = models.TextField(default="Emergency Alert")
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
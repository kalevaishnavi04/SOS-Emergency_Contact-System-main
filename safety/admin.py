from django.contrib import admin
from .models import EmergencyContact, SOSAlert

admin.site.register(EmergencyContact)
admin.site.register(SOSAlert)
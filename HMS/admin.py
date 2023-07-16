from django.contrib import admin
from .models import  Doctor,patient_table,LAB,Patient_LAB


admin.site.register(Doctor)
admin.site.register(patient_table)
admin.site.register(LAB)
admin.site.register(Patient_LAB)

from django.contrib import admin
from .models import  Doctor,patient_table,LAB,Patient_LAB,LAB_Report,OtherCharges,Patient_OtherCharges


admin.site.register(Doctor)
admin.site.register(patient_table)
admin.site.register(LAB)
admin.site.register(Patient_LAB)
admin.site.register(LAB_Report)
admin.site.register(OtherCharges)
admin.site.register(Patient_OtherCharges)

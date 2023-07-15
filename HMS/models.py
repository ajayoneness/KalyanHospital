from django.core.exceptions import ValidationError
from django.db import models


class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)
    qualifications = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    hospital = models.CharField(max_length=200)
    description = models.TextField()
    consultation_fee = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"




class patient_table(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    oe = models.CharField(max_length=20, null=True, blank=True)
    p_name = models.CharField(max_length=50, null=True, blank=True)
    p_age = models.IntegerField(null=True, blank=True)
    mobile_number = models.CharField(max_length=20)
    p_address = models.CharField(max_length=200, null=True, blank=True)
    sex = models.CharField(max_length=20,null=True,blank=True)
    #symptoms = models.CharField(max_length=200, null=True, blank=True)
    admission_date = models.DateTimeField(auto_now_add=True)
    discharge_date = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        self.validate_mobile_number()

    def validate_mobile_number(self):
        import re
        if not re.match(r'^\d{10}$', self.mobile_number):
            raise ValidationError("Invalid mobile number format.")




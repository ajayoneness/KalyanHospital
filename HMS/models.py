from django.core.exceptions import ValidationError
from django.db import models
from decimal import Decimal


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


    def __str__(self):
        return f"{self.p_name}"

    def clean(self):
        super().clean()
        self.validate_mobile_number()

    def validate_mobile_number(self):
        import re
        if not re.match(r'^\d{10}$', self.mobile_number):
            raise ValidationError("Invalid mobile number format.")



class OtherCharges(models.Model):
    oc_name = models.CharField(max_length=200, null=True, blank=True)
    oc_price = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.oc_name}"


class Patient_OtherCharges(models.Model):
    patient = models.ForeignKey(patient_table, on_delete=models.CASCADE)
    othercharge = models.ForeignKey(OtherCharges, on_delete=models.CASCADE)
    billdate = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.patient.p_name} - {self.othercharge.oc_name}"


    def save(self, *args, **kwargs):
        if self.othercharge and self.quantity is not None:
            self.total_price = Decimal(int(self.othercharge.oc_price)) * self.quantity
        super(Patient_OtherCharges, self).save(*args, **kwargs)



class LabCategory(models.Model):
    category = models.CharField(max_length=200, null=True, blank=True)
    sub_category = models.CharField(max_length=200, null=True, blank=True)
    lab_price = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return f"{self.sub_category}"

class LAB(models.Model):
    labcat = models.ForeignKey(LabCategory, on_delete=models.CASCADE)
    lab_name = models.CharField(max_length=200, null=True, blank=True)
    units = models.CharField(max_length=10, null=True, blank=True)
    ref_range = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return f"{self.labcat.category} - {self.labcat.sub_category} - {self.lab_name}"



class Patient_LAB(models.Model):
    patient = models.ForeignKey(patient_table, on_delete=models.CASCADE)
    labCat = models.ForeignKey(LabCategory, on_delete=models.CASCADE)
    testdate = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.patient.p_name}-{self.labCat.sub_category}"

    def save(self, *args, **kwargs):
        if self.labCat and self.quantity is not None:
            self.total_price = Decimal(int(self.labCat.lab_price)) * self.quantity
        super(Patient_LAB, self).save(*args, **kwargs)



class LAB_Report(models.Model):
    P_lab = models.ForeignKey(Patient_LAB, on_delete=models.CASCADE)
    l_report_value = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)


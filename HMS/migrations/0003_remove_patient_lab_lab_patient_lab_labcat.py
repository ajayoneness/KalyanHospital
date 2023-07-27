from django.db import migrations, models

def set_default_labcategory(apps, schema_editor):
    LabCategory = apps.get_model('HMS', 'labcategory')
    try:
        default_labcategory = LabCategory.objects.first()
        if default_labcategory:
            default_value = default_labcategory.pk
        else:
            default_value = None
    except LabCategory.DoesNotExist:
        default_value = None

    PatientLab = apps.get_model('HMS', 'Patient_lab')
    PatientLab.objects.update(labCat=default_value)

class Migration(migrations.Migration):

    dependencies = [
        ('HMS', '0002_rename_billdata_patient_othercharges_billdate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient_lab',
            name='lab',
        ),
        migrations.AddField(
            model_name='patient_lab',
            name='labCat',
            field=models.ForeignKey(
                default=None,  # Set the default value to None
                on_delete=models.CASCADE,
                to='HMS.labcategory',
            ),
        ),
        migrations.RunPython(set_default_labcategory),
    ]

import django
from django.db import models
from django.core.validators import MinValueValidator   
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','myproject.settings')


from datetime import datetime
class ClinicalStudy(models.Model):
    nct_id = models.CharField(max_length=50, unique=True,null=True)
    org_study_id = models.CharField(max_length=50,null=True)
    organization_name = models.CharField(max_length=255,null=True)
    brief_title = models.CharField(max_length=255,null=True)
    official_title = models.CharField(max_length=255,null=True)
    status = models.CharField(max_length=50,null=True)
    status_verified_date = models.DateField(default=None, null=True)
    expanded_access = models.BooleanField(default=False)
    start_date = models.DateField(default=None, null=True, validators=[MinValueValidator(limit_value='2000-01-01')])
    primary_completion_date = models.DateField(default=None, null=True, validators=[MinValueValidator(limit_value='2000-01-01')])
    completion_date = models.DateField(default=None, null=True, validators=[MinValueValidator(limit_value='2000-01-01')])
    study_first_submit_date = models.DateField(default=None, null=True, validators=[MinValueValidator(limit_value='2000-01-01')])
    study_first_submit_qc_date = models.DateField(default=None, null=True, validators=[MinValueValidator(limit_value='2000-01-01')])
    study_first_post_date = models.DateField(default=None, null=True, validators=[MinValueValidator(limit_value='2000-01-01')])
    last_update_submit_date = models.DateField(default=None, null=True, validators=[MinValueValidator(limit_value='2000-01-01')])
    last_update_post_date = models.DateField(default=None, null=True, validators=[MinValueValidator(limit_value='2000-01-01')])

    def clean(self):
        # Ensure start_date, primary_completion_date, completion_date, study_first_post_date,
        # and last_update_post_date have a day component if provided as YYYY-MM
        if self.start_date and len(self.start_date) == 7:
            self.start_date += '-01'
        if self.primary_completion_date and len(self.primary_completion_date) == 7:
            self.primary_completion_date += '-01'
        if self.completion_date and len(self.completion_date) == 7:
            self.completion_date += '-01'
        if self.study_first_post_date and len(self.study_first_post_date) == 7:
            self.study_first_post_date += '-01'
        if self.last_update_post_date and len(self.last_update_post_date) == 7:
            self.last_update_post_date += '-01'
    # def save(self, *args, **kwargs):
    #     self.full_clean()  # Ensure data is validated before saving
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.nct_id

class SponsorCollaborator(models.Model):
    study = models.ForeignKey(ClinicalStudy, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    class_type = models.CharField(max_length=50,null = True)

class Description(models.Model):
    study = models.OneToOneField(ClinicalStudy, on_delete=models.CASCADE)
    brief_summary = models.TextField()
    detailed_description = models.TextField()

class Condition(models.Model):
    study = models.ForeignKey(ClinicalStudy, on_delete=models.CASCADE)
    condition = models.CharField(max_length=255)

class Design(models.Model):
    study = models.OneToOneField(ClinicalStudy, on_delete=models.CASCADE)
    study_type = models.CharField(max_length=50,null=True)
    phases = models.CharField(max_length=50,null=True)
    allocation = models.CharField(max_length=50,null=True)
    intervention_model = models.CharField(max_length=50,null=True)
    intervention_model_description = models.TextField(null=True)
    primary_purpose = models.CharField(max_length=50,null=True)
    masking = models.CharField(max_length=50,null=True)

class Intervention(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    other_names = models.CharField(max_length=255,null=True)
    arm_group_labels = models.CharField(max_length=255)

class ArmGroup(models.Model):
    study = models.ForeignKey(ClinicalStudy, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    description = models.TextField()

class Outcome(models.Model):
    study = models.ForeignKey(ClinicalStudy, on_delete=models.CASCADE)
    measure = models.TextField()
    description = models.TextField()
    time_frame = models.CharField(max_length=255)

class Eligibility(models.Model):
    study = models.OneToOneField(ClinicalStudy, on_delete=models.CASCADE)
    eligibility_criteria = models.TextField(null = True)
    healthy_volunteers = models.BooleanField(default=False)
    sex = models.CharField(max_length=10,null = True)
    minimum_age = models.CharField(max_length=20,null = True)
    maximum_age = models.CharField(max_length=20,null = True)
    stdAges = models.CharField(max_length = 100,default='all',null = True)

class ContactLocation(models.Model):
    study = models.OneToOneField(ClinicalStudy, on_delete=models.CASCADE)
    facility = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100,null = True)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Reference(models.Model):
    study = models.ForeignKey(ClinicalStudy, on_delete=models.CASCADE)
    pmid = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    citation = models.TextField()

class MiscInfo(models.Model):
    study = models.OneToOneField(ClinicalStudy, on_delete=models.CASCADE)
    version_holder = models.CharField(max_length=20)

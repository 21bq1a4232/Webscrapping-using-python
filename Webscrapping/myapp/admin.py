from django.contrib import admin
from .models import ClinicalStudy, SponsorCollaborator, Description, Condition, Design, Intervention, ArmGroup, Outcome, Eligibility, ContactLocation, Reference, MiscInfo

admin.site.register(ClinicalStudy)
admin.site.register(SponsorCollaborator)
admin.site.register(Description)
admin.site.register(Condition)
admin.site.register(Design)
admin.site.register(Intervention)
admin.site.register(ArmGroup)
admin.site.register(Eligibility)
admin.site.register(Outcome)
admin.site.register(ContactLocation)
admin.site.register(Reference)
admin.site.register(MiscInfo)

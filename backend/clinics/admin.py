from django.contrib import admin
from clinics.models import Clinic, Doctor, Schedule

admin.site.register(Clinic)
admin.site.register(Doctor)
admin.site.register(Schedule)


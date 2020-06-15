from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(HospitalData)
# admin.site.register(PatientData)

# admin.site.register(UserProfile)


class PatientDataAdmin(admin.ModelAdmin):
    readonly_fields = ('patient_name', 'patient_number')


admin.site.register(PatientData, PatientDataAdmin)

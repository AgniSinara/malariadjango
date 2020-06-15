from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class HospitalData(models.Model):
    hospital_name = models.TextField()
    hospital_address = models.TextField()

class RegisterData(models.Model):
    registration_number = models.TextField(null=True)
    hospital_name = models.ForeignKey(HospitalData, on_delete=models.SET_NULL,
                                    related_name="current_hospital_RegisterData", null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.TextField(null=True)
    registration_number = models.TextField(null=True)
    current_hospital = models.ForeignKey(HospitalData, on_delete=models.SET_NULL,
                                        related_name="current_hospital_UserProfile", null=True)
    user_type = models.IntegerField(null=True)  # 1=Dokter, 2=Tenaga Medis, 3=Pasien
    patient_number = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        if self.user_type == 3:
            self.patient_number = self.user.id
        self.full_name = self.user.first_name + ' ' + self.user.last_name

        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class PatientData(models.Model):
    patient = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                related_name="patient_patient_data", null=True)
    patient_name = models.TextField(editable=False)
    patient_number = models.IntegerField(null=True, editable=False)
    medical_personnel = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                          related_name="med_per_patient_data", null=True)
    assigned_doctor = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                        related_name="ass_doc_patient_data", null=True)
    input_time = models.DateTimeField(auto_now_add=True)
    input_place = models.TextField(null=True)
    image = models.TextField(null=True)
    result = models.IntegerField(null=True)
    status = models.TextField(null=True)
    doctor_name = models.TextField(null=True)
    medical_personnel_name = models.TextField(null=True)

    def save(self, *args, **kwargs):
        self.patient_name = self.patient.full_name
        self.patient_number = self.patient.user.id
        self.doctor_name = self.assigned_doctor.full_name
        self.medical_personnel_name = self.medical_personnel.full_name

        super(PatientData, self).save(*args, **kwargs)

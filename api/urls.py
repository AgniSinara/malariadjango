from django.urls import path

from .views import *


urlpatterns = [
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('me', my_profile, name='my_profile'),
    path('patients', get_patients, name='patient_data'),
    path('add-patient-data', add_patient_data, name='add_patient_data'),
    path('patient-data', patient_data, name='patient_data'),
    path('patient-data/<int:id>', patient_data_detail, name='patient_data_detail'),
    path('confirm-case', confirm_case, name='confirm_case'),
    path('test-dl', img_test, name='ss')
]

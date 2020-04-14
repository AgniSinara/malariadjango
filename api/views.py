from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import *
from .models import *
from .utils import *

from classifier.ml.ml_model import *


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)

    user_type = {
        1: 'Dokter',
        2: 'Tenaga Medis',
        3: 'Pasien'
    }
    full_name = user.first_name + ' ' + user.last_name

    return Response({
        'token': token.key,
        'userId': user.pk,
        'username': user.username,
        'fullName': full_name,
        'userType': user_type[user.profile.user_type]
    }, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    first_name = request.data.get('firstName')
    last_name = request.data.get('lastName')
    user_type = request.data.get('userType')

    user_serializers = UserSerializer(data=request.data)
    if user_serializers.is_valid() and user_type in [1, 2, 3]:
        user = User.objects.create_user(username=username,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name)

        user.profile.user_type = user_type
        user.save()

        return Response({
            'status': 1,
            'message': 'User successfully created'
        })
    else:
        return Response({
            'status': 0,
            'message': 'Please provide all required data'
        }, status=HTTP_400_BAD_REQUEST)




@csrf_exempt
@api_view(["GET"])
def my_profile(request):
    user = request.user
    username = user.username
    user_type = user.profile.user_type
    full_name = user.first_name + ' ' + user.last_name

    return Response({
        'username': username,
        'fullName': full_name,
        'userType': user_type
    }, status=HTTP_200_OK)


# Get patient list
@csrf_exempt
@api_view(["GET"])
# @permission_classes((AllowAny,))
def get_patients(request):
    # get current user
    user = request.user
    if user:
        # check if user is medstaff
        if user.profile.user_type == 2:
            # get all patient from user profile table
            queryset = UserProfile.objects.filter(user_type=3)
            patients = []

            # arrange patient data
            for patient in queryset:
                username = patient.user.username
                user_type = patient.user_type
                full_name = patient.user.first_name + ' ' + patient.user.last_name
                patient_data = {
                    'id': patient.user.id,
                    'username': username,
                    'fullName': full_name,
                    'userType': user_type
                }
                patients.append(patient_data)

            return Response({
                'status': 1,
                'patientData': patients
            })
        else:
            # if user is not medstaff
            return Response({
                'status': 0,
                'message': 'access denied'
            })


# submit patient data
@csrf_exempt
@api_view(["POST"])
# @permission_classes((AllowAny,))
def add_patient_data(request):
    # get current user
    user = request.user
    if user:
        # check if user is medstaff
        if user.profile.user_type == 2:
            patient_id = request.data.get('patientId')
            patient = UserProfile.objects.get(patient_number=patient_id)
            if patient:
                patient_data = PatientData(
                    patient=patient,
                    patient_name=patient.user.first_name + ' ' + patient.user.last_name,
                    patient_number=patient_id,
                    medical_personnel=user.profile,
                    assigned_doctor=user.profile,  # temp fix
                    input_place=request.data.get('inputPlace'),
                    image=request.data.get('imageUrl'),
                    result=-1,  # temp fix
                    status='unconfirmed'
                )

                patient_data.save()

                return Response({
                    'status': 1
                })


@csrf_exempt
@api_view(["POST", "GET"])
def patient_data(request):
    user = request.user

    # If user is medstaff
    if user.profile.user_type == 2:
        # If medstaff is add new data
        if request.method == "POST":
            patient_id = request.data.get('patientId')
            patient = UserProfile.objects.get(patient_number=patient_id)
            # If assigned patient is valid
            if patient:
                # Get doctor
                doctor_id = get_doctor()
                print(doctor_id)
                queryset = User.objects.get(id=doctor_id)
                doctor = queryset.profile


                url = request.data.get('imageUrl')
                hasil = model_predict(url)
                classes = [1, 0]
                result = str('{}'.format(classes[np.argmax(hasil[0])]))


                patient_data = PatientData(
                    patient=patient,
                    patient_name=patient.user.first_name + ' ' + patient.user.last_name,
                    patient_number=patient_id,
                    medical_personnel=user.profile,
                    assigned_doctor=doctor,  # temp fix
                    input_place=request.data.get('inputPlace'),
                    image=url,
                    result=int(result),  # temp fix
                    status='unconfirmed'
                )

                patient_data.save()

                return Response({
                    'status': 1
                })
            else:
                return Response({
                    'status': 0
                })
        # If medstaff request data
        elif request.method == "GET":
            queryset = PatientData.objects.all()

            serializer = PatientDataWriteSerializer(queryset, many=True)
            return Response({
                'status': 1,
                'data': serializer.data
            })
    # If user is doctor and he/she is requesting data
    elif user.profile.user_type == 1 and request.method == 'GET':
        queryset = PatientData.objects.filter(assigned_doctor=user.profile)

        serializer = PatientDataWriteSerializer(queryset, many=True)
        return Response({
            'status': 1,
            'data': serializer.data
        })

    elif user.profile.user_type == 3 and request.method == 'GET':
        queryset = PatientData.objects.filter(patient=user.profile)

        serializer = PatientDataWriteSerializer(queryset, many=True)
        return Response({
            'status': 1,
            'data': serializer.data
        })



@csrf_exempt
@api_view(["POST"])
def change_result(request):
    user = request.user

    # If user is doctor
    if user.profile.user_type == 1:
        patient_data_id = request.data.get('patientDataId')
        result = request.data.get('result')

        try:
            patient_data = PatientData.objects.get(id=patient_data_id)

            if patient_data.assigned_doctor == user.profile:
                patient_data.result = result
                # patient_data.status = 'confirmed'
                patient_data.save()

                serializer = PatientDataWriteSerializer(patient_data)
                return Response({
                    'status': 1,
                    'data': serializer.data
                })
            else:
                return Response({
                    'status': 0,
                    'message': 'koe sopo?'
                })

        except:
            return Response({
                'status': 0,
            })

    else:
        return Response({
            'status': 0,
            'message': 'koe sopo?'
        })


@csrf_exempt
@api_view(["POST"])
def confirm_case(request):
    user = request.user

    # If user is doctor
    if user.profile.user_type == 1:
        patient_data_id = request.data.get('patientDataId')
        status = request.data.get('status')
        try:
            patient_data = PatientData.objects.get(id=patient_data_id)

            if patient_data.assigned_doctor == user.profile:
                patient_data.status = status
                patient_data.save()

                serializer = PatientDataWriteSerializer(patient_data)
                return Response({
                    'status': 1,
                    'data': serializer.data
                })
            else:
                return Response({
                    'status': 0,
                    'message': 'koe sopo?'
                })

        except:
            return Response({
                'status': 0,
            })

    else:
        return Response({
            'status': 0,
            'message': 'koe sopo?'
        })




@csrf_exempt
@api_view(["GET"])
def patient_data_detail(request, id):
    user_type = request.user.profile.user_type

    try:
        patient_data = PatientData.objects.get(id=id)

        if (user_type == 1 and patient_data.assigned_doctor == request.user.profile) or user_type == 2 or (
                request.user.profile == patient_data.patient):
            serializer = PatientDataWriteSerializer(patient_data)
            return Response({
                'status': 1,
                'data': serializer.data
            })
        else:
            return Response({
                'status': 0,
                'message': 'koe sopo? '
            })
    except:
        return Response({
            'status': 0,
        })

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def img_test(request):
    url = request.data.get('url')

    hasil = model_predict(url)
    classes = [1, 0]
    result = str('{}'.format(classes[np.argmax(hasil[0])]))

    return Response({
        'status': 0,
        'hasil': int(result)
    })


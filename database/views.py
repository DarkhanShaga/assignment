import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import (
    User, Caregiver, Member, Address, Job, JobApplication, Appointment
)


def model_to_dict(instance):
    if instance is None:
        return None
    
    data = {}
    for field in instance._meta.fields:
        value = getattr(instance, field.name)
        if field.many_to_one or field.one_to_one:
            if value is not None:
                fk_id = getattr(instance, field.attname)
                data[field.name] = fk_id
            else:
                data[field.name] = None
        elif hasattr(value, '__float__') and not isinstance(value, bool):
            value = float(value)
            data[field.name] = value
        elif hasattr(value, 'isoformat'):
            value = value.isoformat()
            data[field.name] = value
        else:
            data[field.name] = value
    return data

user_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, read_only=True),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email address'),
        'given_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
        'surname': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
        'city': openapi.Schema(type=openapi.TYPE_STRING, description='City'),
        'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
        'profile_description': openapi.Schema(type=openapi.TYPE_STRING, description='Profile description'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
    },
    required=['email', 'password']
)

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all users",
    responses={200: openapi.Response('List of users', user_schema)}
)
@swagger_auto_schema(
    method='post',
    operation_description="Create a new user",
    request_body=user_schema,
    responses={201: openapi.Response('User created', user_schema), 400: 'Bad request'}
)
@csrf_exempt
@api_view(['GET', 'POST'])
def user_list_create(request):
    if request.method == 'GET':
        users = User.objects.all()
        data = [model_to_dict(user) for user in users]
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.create(**data)
            return JsonResponse(model_to_dict(user), status=201)
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a specific user by ID",
    responses={200: openapi.Response('User details', user_schema), 404: 'User not found'}
)
@swagger_auto_schema(
    method='put',
    operation_description="Update a specific user",
    request_body=user_schema,
    responses={200: openapi.Response('User updated', user_schema), 400: 'Bad request', 404: 'User not found'}
)
@swagger_auto_schema(
    method='delete',
    operation_description="Delete a specific user",
    responses={204: 'User deleted', 404: 'User not found'}
)
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse(model_to_dict(user))
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(user, key, value)
            user.save()
            return JsonResponse(model_to_dict(user))
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=204)

caregiver_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'caregiver_user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID (foreign key)'),
        'photo': openapi.Schema(type=openapi.TYPE_STRING, description='Photo URL or base64'),
        'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Gender'),
        'caregiving_type': openapi.Schema(type=openapi.TYPE_STRING, enum=['babysitter', 'caregiver for elderly', 'playmate for children']),
        'hourly_rate': openapi.Schema(type=openapi.TYPE_NUMBER, description='Hourly rate'),
    },
    required=['caregiver_user_id', 'caregiving_type']
)

@swagger_auto_schema(method='get', operation_description="List all caregivers")
@swagger_auto_schema(method='post', operation_description="Create a new caregiver", request_body=caregiver_schema)
@csrf_exempt
@api_view(['GET', 'POST'])
def caregiver_list_create(request):
    if request.method == 'GET':
        caregivers = Caregiver.objects.all()
        data = [model_to_dict(caregiver) for caregiver in caregivers]
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            caregiver = Caregiver.objects.create(**data)
            return JsonResponse(model_to_dict(caregiver), status=201)
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@swagger_auto_schema(method='get', operation_description="Get a specific caregiver")
@swagger_auto_schema(method='put', operation_description="Update a caregiver", request_body=caregiver_schema)
@swagger_auto_schema(method='delete', operation_description="Delete a caregiver")
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def caregiver_detail(request, caregiver_user_id):
    try:
        caregiver = Caregiver.objects.get(caregiver_user_id=caregiver_user_id)
    except Caregiver.DoesNotExist:
        return JsonResponse({'error': 'Caregiver not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse(model_to_dict(caregiver))
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(caregiver, key, value)
            caregiver.save()
            return JsonResponse(model_to_dict(caregiver))
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        caregiver.delete()
        return JsonResponse({'message': 'Caregiver deleted successfully'}, status=204)

member_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'member_user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID (foreign key)'),
        'house_rules': openapi.Schema(type=openapi.TYPE_STRING, description='House rules'),
        'dependent_description': openapi.Schema(type=openapi.TYPE_STRING, description='Dependent description'),
    },
    required=['member_user_id']
)

@swagger_auto_schema(method='get', operation_description="List all members")
@swagger_auto_schema(method='post', operation_description="Create a new member", request_body=member_schema)
@csrf_exempt
@api_view(['GET', 'POST'])
def member_list_create(request):
    if request.method == 'GET':
        members = Member.objects.all()
        data = [model_to_dict(member) for member in members]
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            member = Member.objects.create(**data)
            return JsonResponse(model_to_dict(member), status=201)
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@swagger_auto_schema(method='get', operation_description="Get a specific member")
@swagger_auto_schema(method='put', operation_description="Update a member", request_body=member_schema)
@swagger_auto_schema(method='delete', operation_description="Delete a member")
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def member_detail(request, member_user_id):
    try:
        member = Member.objects.get(member_user_id=member_user_id)
    except Member.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse(model_to_dict(member))
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(member, key, value)
            member.save()
            return JsonResponse(model_to_dict(member))
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        member.delete()
        return JsonResponse({'message': 'Member deleted successfully'}, status=204)

address_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'member_user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Member ID (foreign key)'),
        'house_number': openapi.Schema(type=openapi.TYPE_STRING, description='House number'),
        'street': openapi.Schema(type=openapi.TYPE_STRING, description='Street name'),
        'town': openapi.Schema(type=openapi.TYPE_STRING, description='Town/City'),
    },
    required=['member_user_id']
)

@swagger_auto_schema(method='get', operation_description="List all addresses")
@swagger_auto_schema(method='post', operation_description="Create a new address", request_body=address_schema)
@csrf_exempt
@api_view(['GET', 'POST'])
def address_list_create(request):
    if request.method == 'GET':
        addresses = Address.objects.all()
        data = [model_to_dict(address) for address in addresses]
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            address = Address.objects.create(**data)
            return JsonResponse(model_to_dict(address), status=201)
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@swagger_auto_schema(method='get', operation_description="Get a specific address")
@swagger_auto_schema(method='put', operation_description="Update an address", request_body=address_schema)
@swagger_auto_schema(method='delete', operation_description="Delete an address")
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def address_detail(request, member_user_id):
    try:
        address = Address.objects.get(member_user_id=member_user_id)
    except Address.DoesNotExist:
        return JsonResponse({'error': 'Address not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse(model_to_dict(address))
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(address, key, value)
            address.save()
            return JsonResponse(model_to_dict(address))
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        address.delete()
        return JsonResponse({'message': 'Address deleted successfully'}, status=204)

job_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'job_id': openapi.Schema(type=openapi.TYPE_INTEGER, read_only=True),
        'member_user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Member ID (foreign key)'),
        'required_caregiving_type': openapi.Schema(type=openapi.TYPE_STRING, enum=['babysitter', 'caregiver for elderly', 'playmate for children']),
        'other_requirements': openapi.Schema(type=openapi.TYPE_STRING, description='Other requirements'),
        'date_posted': openapi.Schema(type=openapi.FORMAT_DATE, description='Date posted'),
    },
    required=['member_user_id', 'required_caregiving_type']
)

@swagger_auto_schema(method='get', operation_description="List all jobs")
@swagger_auto_schema(method='post', operation_description="Create a new job", request_body=job_schema)
@csrf_exempt
@api_view(['GET', 'POST'])
def job_list_create(request):
    if request.method == 'GET':
        jobs = Job.objects.all()
        data = [model_to_dict(job) for job in jobs]
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            job = Job.objects.create(**data)
            return JsonResponse(model_to_dict(job), status=201)
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@swagger_auto_schema(method='get', operation_description="Get a specific job")
@swagger_auto_schema(method='put', operation_description="Update a job", request_body=job_schema)
@swagger_auto_schema(method='delete', operation_description="Delete a job")
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def job_detail(request, job_id):
    try:
        job = Job.objects.get(job_id=job_id)
    except Job.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse(model_to_dict(job))
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(job, key, value)
            job.save()
            return JsonResponse(model_to_dict(job))
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        job.delete()
        return JsonResponse({'message': 'Job deleted successfully'}, status=204)

job_application_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'caregiver_user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Caregiver ID (foreign key)'),
        'job_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Job ID (foreign key)'),
        'date_applied': openapi.Schema(type=openapi.FORMAT_DATE, description='Date applied'),
    },
    required=['caregiver_user_id', 'job_id']
)

@swagger_auto_schema(method='get', operation_description="List all job applications")
@swagger_auto_schema(method='post', operation_description="Create a new job application", request_body=job_application_schema)
@csrf_exempt
@api_view(['GET', 'POST'])
def job_application_list_create(request):
    if request.method == 'GET':
        applications = JobApplication.objects.all()
        data = [model_to_dict(app) for app in applications]
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            application = JobApplication.objects.create(**data)
            return JsonResponse(model_to_dict(application), status=201)
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@swagger_auto_schema(method='get', operation_description="Get a specific job application")
@swagger_auto_schema(method='put', operation_description="Update a job application", request_body=job_application_schema)
@swagger_auto_schema(method='delete', operation_description="Delete a job application")
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def job_application_detail(request, caregiver_user_id, job_id):
    try:
        application = JobApplication.objects.get(
            caregiver_user_id=caregiver_user_id,
            job_id=job_id
        )
    except JobApplication.DoesNotExist:
        return JsonResponse({'error': 'Job application not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse(model_to_dict(application))
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(application, key, value)
            application.save()
            return JsonResponse(model_to_dict(application))
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        application.delete()
        return JsonResponse({'message': 'Job application deleted successfully'}, status=204)

appointment_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'appointment_id': openapi.Schema(type=openapi.TYPE_INTEGER, read_only=True),
        'caregiver_user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Caregiver ID (foreign key)'),
        'member_user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Member ID (foreign key)'),
        'appointment_date': openapi.Schema(type=openapi.FORMAT_DATE, description='Appointment date'),
        'appointment_time': openapi.Schema(type=openapi.TYPE_STRING, description='Appointment time (HH:MM:SS)'),
        'work_hours': openapi.Schema(type=openapi.TYPE_NUMBER, description='Work hours'),
        'status': openapi.Schema(type=openapi.TYPE_STRING, enum=['Pending', 'Confirmed', 'Declined'], description='Appointment status'),
    },
    required=['caregiver_user_id', 'member_user_id', 'appointment_date', 'appointment_time', 'work_hours']
)

@swagger_auto_schema(method='get', operation_description="List all appointments")
@swagger_auto_schema(method='post', operation_description="Create a new appointment", request_body=appointment_schema)
@csrf_exempt
@api_view(['GET', 'POST'])
def appointment_list_create(request):
    if request.method == 'GET':
        appointments = Appointment.objects.all()
        data = [model_to_dict(appointment) for appointment in appointments]
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            appointment = Appointment.objects.create(**data)
            return JsonResponse(model_to_dict(appointment), status=201)
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@swagger_auto_schema(method='get', operation_description="Get a specific appointment")
@swagger_auto_schema(method='put', operation_description="Update an appointment", request_body=appointment_schema)
@swagger_auto_schema(method='delete', operation_description="Delete an appointment")
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def appointment_detail(request, appointment_id):
    try:
        appointment = Appointment.objects.get(appointment_id=appointment_id)
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse(model_to_dict(appointment))
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(appointment, key, value)
            appointment.save()
            return JsonResponse(model_to_dict(appointment))
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        appointment.delete()
        return JsonResponse({'message': 'Appointment deleted successfully'}, status=204)

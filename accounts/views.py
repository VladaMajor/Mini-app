from accounts.models import AdditionalUserData, Device, Sim, M2M_Device_Sim, Permission_type, Permissions
from events.models import EventInvitation, Event
from chat.models import chatRoom
from django.contrib.auth.models import User
from .serializers import UserSerializer, PermissionsSeriallizer
from django.conf import settings
from rest_framework import generics, viewsets, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.settings import api_settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password
from phonenumbers.phonenumberutil import (
    region_code_for_country_code,
    region_code_for_number,
)
from rest_framework.views import APIView
from rest_framework.response import Response
import uuid
import hashlib
import json
import phonenumbers
import pycountry
import requests
from random import randint

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class CheckUserVerifiedRegisterdViewSet(APIView):  # CHECKS IF USER IS VERIFIED AND REGISTERD
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        if data['username'] == 'no username':
            return JsonResponse({'status': 'not_registerd'})
        else:
            try:
                user = User.objects.get(username=data['username'])
                sim_objects = Sim.objects.get(fk_account=user)
                if sim_objects.verified_sim_code == '0':
                    token = jwt_encode_handler(jwt_payload_handler(user))
                    userAdd = AdditionalUserData.objects.get(user=user)
                    pn = phonenumbers.parse(sim_objects.phone_number)
                    countryCode = pn.country_code
                    return JsonResponse({
                        'token': token, 'username': user.username, 'user_id': user.id,
                        'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                        'avatar': userAdd.avatar.url, 'phone_number': sim_objects.phone_number,
                        'country_code': countryCode, 'city': userAdd.city, 'street': userAdd.street,
                        'state': userAdd.state, 'home_number': userAdd.home_number,
                        'notifications': userAdd.notification, 'verified_email': userAdd.verified_email})
                else:
                    data = {
                        'number': sim_objects.phone_number,
                        'message': 'Your Events confirmation code is : ' + sim_objects.verified_sim_code,
                        'type': 'verification code',
                        'uuid': 'events',
                        'status': 0, }
                    r = requests.post(url=settings.SMSSERVER, data=data)
                    return JsonResponse({'status': 'not_verified', 'username': user.username})
            except:
                return JsonResponse({'status': 'not_registerd'})

class UserCreateAPIView(generics.CreateAPIView):  # CREATES NEW USER
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            check_if_user_have_phone_registerd = Sim.objects.get(phone_number=data['phone'])
            if check_if_user_have_phone_registerd:
                user = User.objects.get(id=check_if_user_have_phone_registerd.fk_account.id)
                verification_code = str(randint(100000, 999999))
                check_if_user_have_phone_registerd.verified_sim_code = verification_code
                check_if_user_have_phone_registerd.save()
                return JsonResponse({'status': 'not_verified', 'username': user.username})
        except:
            username = uuid.uuid1()  # make a UUID based on the host ID and current time
            username_hashed = hashlib.md5((str(username)).encode())  # encode() : Converts the string into
            username_hashed = username_hashed.hexdigest()            # bytes to be acceptable by hash function.
            user = User.objects.create_user(
                username=username_hashed,
                password='123456',
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            device = Device.objects.create(
                fk_account=AdditionalUserData.objects.get(user=user),
                device_uuid=data['device_uuid'],
                vendor=data['device_vender'],
                model=data['device_model'],
                os=data['device_platform']
            )
            pn = phonenumbers.parse(str(data['phone']))
            country = pycountry.countries.get(alpha_2=region_code_for_number(pn))
            verification_code = str(randint(100000, 999999))
            sim = Sim.objects.create(
                fk_account=user,
                country=country.name,
                phone_number=data['phone'],
                verified_sim_code=verification_code
            )
            M2M_Device_Sim.objects.create(
                id_sim=sim,
                id_device=device,
                fk_account=user.id
            )
            data = {
                'number': sim.phone_number,
                'message': 'Your Events confirmation code is : ' + verification_code,
                'type': 'reset password',
                'uuid': 'events',
                'status': 0, }
            r = requests.post(url=settings.SMSSERVER, data=data)
            return JsonResponse({'status': 'not_verified', 'username': username_hashed})

class SetCodeToZero(APIView):  # SETS SIM VERIFICATION CODE TO 0
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            data = request.data
            user = User.objects.get(username=data['username'])
            try:
                sim_object = Sim.objects.get(verified_sim_code=data['code'], fk_account=user)
                sim_object.verified_sim_code = 0
                sim_object.save()
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                user_additional = AdditionalUserData.objects.get(user=user)
                phone_number = Sim.objects.filter(fk_account=user).first()
                phone_numbers = Sim.objects.filter(fk_account=user)
                invitations = EventInvitation.objects.filter(sim_phone_number=sim_object)
                for invite in invitations:
                    invite.fk_account = user
                    invite.save()
                return JsonResponse({
                    'token': token, 'user_id': user.id, 'username': user.username,
                    'first_name': user.first_name, 'last_name': user.last_name,
                    'avatar': user_additional.avatar.url, 'phone_number': phone_number.phone_number})
            except:
                return JsonResponse({'code': 'Error'})

class ChangePhoneNumber(generics.ListCreateAPIView):  # CHANGES USER SIM PHONE NUMBER
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.get(username=data['username'])
        sim_object = Sim.objects.get(fk_account=user)
        sim_object.phone_number = data['phone_number']
        sim_object.save()
        data = {
            'number': sim_object.phone_number,
            'message': 'Your Events verification code is : ' + sim_object.verified_sim_code,
            'type': 'verification code',
            'uuid': 'events',
            'status': 0, }
        r = requests.post(url=settings.SMSSERVER, data=data)
        return JsonResponse({'phone': 'changed'})

class ResendConfirmationCode(APIView):  # SEND'S SIM CONFIRMATION CODE TO USER
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.get(username=data['username'])
        phone_number = Sim.objects.filter(fk_account=user)
        phone = phone_number[0].phone_number
        data = {
            'number': phone,
            'message': 'Your Events confirmation code is : ' + phone_number[0].verified_sim_code,
            'type': 'verification code',
            'uuid': 'events',
            'status': 0, }
        r = requests.post(url=settings.SMSSERVER, data=data)
        return JsonResponse({'status': 'sent'})

class WhoCanEdit(APIView):  # RETURNS LIST OF USER WHIT PERMISSION TO EDIT EVENT
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        perms = Permissions.objects.filter(row_id=data)
        serializer = PermissionsSeriallizer(perms, many=True)
        return Response(serializer.data)

class UserFirebaseToken(APIView):  # SAVES FIREBASE TOKEN OF USER
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        try:
            userToken = AdditionalUserData.objects.get(user_id=data['user_id'])
            userToken.firebaseToken = data['token']
            userToken.save()
            return JsonResponse({'status': 'OK'})
        except:
            return JsonResponse({'status': 'Error saving token!'})

class UpdateUserProfile(APIView):  # UPDATES USER PROFILE
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        print(data)
        user = User.objects.get(id=data['user_id'])
        userAddData = AdditionalUserData.objects.get(user=user)
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.save()
        if data['avatar'] != '':
            userAddData.avatar = data['avatar']
        userAddData.state = data['state']
        userAddData.street = data['street']
        userAddData.city = data['city']
        userAddData.home_number = data['home_number']
        if data['notifications'] == 'true':
            userAddData.notification = True
        if data['notifications'] == 'false':
            userAddData.notification = False
        userAddData.save()
        return JsonResponse({
            'status': 'updated',
            'avatar': userAddData.avatar.url,
            'verified_email': userAddData.verified_email})

class UserPermissions(APIView):  # CHECKS IF USER HAVE PERMISSION FOR EDITING EVENT
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        user = User.objects.get(id=data['fk_account'])
        try:
            event = Permissions.objects.get(row_id=data['fk_event'], fk_account=user)
            return JsonResponse({'permission_type': event.fk_permission_type.name})
        except:
            return JsonResponse({'permission_type': 'None'})

class SendNotifications(APIView):  # API FOR SENDING NOTIFICATION, NEEDS TO BE FINNISHED
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        url = 'https://fcm.googleapis.com/fcm/send'
        headers = {
            'Authorization': '#################################',
            'Content-Type': 'application/json',
        }
        data = {
            "to": 'all',
            "notification":
                {
                    "title": 'Obaveštenje!',
                    "body": 'Venčanje',
                    "content_available": "true",
                    "priority": "high",
                },
            "data":
                {
                    "title": 'Obavestenje',
                    "body": 'Vencanje',
                }
        }
        a = requests.post(url, headers=headers, data=json.dumps(data))
        return JsonResponse({'status': 'sent'})

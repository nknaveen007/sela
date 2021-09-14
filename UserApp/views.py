import uuid
from django.http import response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse


from UserApp.models import UserData
from UserApp.serializers import UserSerialiser
from Helper.sendotp import sendOtpHelper, verifyOtpHelper


@csrf_exempt
def userverify_otp(request, number=0, code=0):
    print(number, code)
    fullnumber = '+'+number
    if request.method == 'GET':
        result = verifyOtpHelper(fullnumber, code)

        if result['status'] == 'approved':
            int_number = int(number)

            try:
                user = UserData.objects.get(PhoneNumber=number[2:])
                userserialiser = UserSerialiser(user)
                if userserialiser.data['PhoneNumber']:
                    return JsonResponse({'Status': True, 'UserDetails': userserialiser.data}, safe=False)

            except Exception as e:
                er = str(e)
                print(er, e)
                if er == 'UserData matching query does not exist.':
                    userdata_serializer = UserSerialiser(
                        data={'PhoneNumber': number[2:]})
                    if userdata_serializer.is_valid():
                        userdata_serializer.save()
                        user = UserData.objects.get(PhoneNumber=number[2:])
                        userdata_serializer = UserSerialiser(user)
                        return JsonResponse({'Status': True, 'Registered': False, 'UserData': userdata_serializer.data}, safe=False, status=200)
                    return JsonResponse('Failed to Add', safe=False)
                return JsonResponse({'Status': False, 'Message': 'Something wrong'}, safe=False, status=500)

        else:
            return JsonResponse({'Status': False, 'Message': 'Phone number or OTP is wrong'}, safe=False)


@csrf_exempt
def usersend_otp(request, id=0):

    if request.method == 'GET':
        fullnumber = '+'+id
        result = sendOtpHelper(fullnumber)
        return JsonResponse(result, safe=False)


@csrf_exempt
def User_data(request, id=0):
    try:
        if request.method == 'GET':
            if id != 0:
                users = UserData.objects.get(UserId=id)
                users_serializer = UserSerialiser(users)
                return JsonResponse(users_serializer.data, safe=False)
            else:
                users = UserData.objects.all()
                users_serializer = UserSerialiser(users, many=True)
                return JsonResponse(users_serializer.data, safe=False)

        elif request.method == 'PUT':
            users_data = JSONParser().parse(request)
            user = UserData.objects.get(UserId=id)
            if user.UserStatus == 1 and user.Name == '':
                uniqueId = str(uuid.uuid4())
                selaId = 'SELA-'+uniqueId
                updatedData = {'SelaId': selaId,
                               'Name': users_data['Name'], 'UserStatus': 0}
                user_serializer = UserSerialiser(user, data=updatedData)
                if user_serializer.is_valid():
                    user_serializer.save()
                    user = UserData.objects.get(UserId=id)
                    user_serializer = UserSerialiser(user)
                    return JsonResponse({'updated': 'Successfully', 'Status': 0, 'user data': user_serializer.data}, safe=False)
                return JsonResponse('Failed to Update', safe=False)

            else:
                user_serializer = UserSerialiser(
                    user, data={'Name': users_data['Name']})
                if user_serializer.is_valid():
                    user_serializer.save()
                    return JsonResponse({'updated': 'Successfully'}, safe=False)
                return JsonResponse('Failed to Update', safe=False)

        elif request.method == 'DELETE':
            user = UserData.objects.get(UserId=id)
            user.delete()
            return JsonResponse('Deleted Successfully', safe=False)

    except Exception as e:
        er_str = str(e)
        return JsonResponse(er_str, safe=False, status=400)

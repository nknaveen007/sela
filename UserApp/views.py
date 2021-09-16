import uuid
from django.http import response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
import re
import random


from UserApp.models import UserData, Otp
from UserApp.serializers import UserSerialiser, OtpSerialiser
from Helper.sendotp import sendOtpHelper, verifyOtpHelper


def isValid(s):
    Pattern = re.compile("(0|91)?[7-9][0-9]{9}")
    return Pattern.match(s)


@csrf_exempt
def userverify_otp(request, number=0, code=0):
    otpValid = None
    print(number, code)
    fullnumber = '+'+number
    if request.method == 'GET':
      #  result = verifyOtpHelper(fullnumber, code)
        #  if result['status'] == 'approved':
      #      int_number = int(number)
        valid = isValid(number)

        if valid:

            try:
                otpUser = Otp.objects.get(number=number[2:])

                if code == otpUser.otp:

                    otpValid = True
                    if otpValid:
                        try:
                            user = UserData.objects.get(PhoneNumber=number[2:])
                            userserialiser = UserSerialiser(user)
                            if userserialiser.data['PhoneNumber']:
                                return JsonResponse({'Status': True, 'Message': 'Otp verified successfully', 'User': {'UserId': userserialiser.data['UserId'], 'UserStatus': userserialiser.data['UserStatus']}}, safe=False)

                        except Exception as e:
                            er = str(e)
                            print(er, e)
                            if er == 'UserData matching query does not exist.':
                                userdata_serializer = UserSerialiser(
                                    data={'PhoneNumber': number[2:]})
                                if userdata_serializer.is_valid():
                                    userdata_serializer.save()
                                    user = UserData.objects.get(
                                        PhoneNumber=number[2:])
                                    userdata_serializer = UserSerialiser(user)
                                    return JsonResponse({'Status': True, 'Message': 'Otp verified successfully', 'User': {'UserId': userdata_serializer.data['UserId'], 'UserStatus': userdata_serializer.data['UserStatus']}}, safe=False, status=200)
                                return JsonResponse({'Status': False, 'Message': 'Failed to Update'}, safe=False, status=400)
                            return JsonResponse({'Status': False, 'Message': 'Something wrong'}, safe=False, status=500)
                else:
                    return JsonResponse({'Status': False, 'Message': 'Verification failed!'}, safe=False, status=400)
            except:
                return JsonResponse({'Status': False, 'Message': 'Phone number is wrong'}, safe=False, status=400)

      #  elif result['status'] == 'expired' or result['status'] == 'when the max attempts to check a code have been reached':
            #  return JsonResponse({'Status': False, 'Message': result['status']}, safe=False)
      #  else:
            #  return JsonResponse({'Status': False, 'Message': 'Phone number or OTP is wrong'}, safe=False)
        else:
            return JsonResponse({'Status': False, 'Message': 'Phone number or OTP is wrong'}, safe=False, status=400)


@csrf_exempt
def usersend_otp(request, id=0):

    if request.method == 'GET':
        fullnumber = '+'+id
        # result = sendOtpHelper(fullnumber)
        # return JsonResponse(result, safe=False)
        if isValid(id):
            code = random.randint(1000, 9999)
            otpUser = None

            try:

                otpUser = Otp.objects.get(number=id[2:])
                otp_Seriyalizer = OtpSerialiser(
                    otpUser, {'number': id[2:], 'otp': code})
                otp_Seriyalizer.save()

                return JsonResponse({'Status': True, 'Message': 'OTP sent to your given number +'+id, 'OtpCode': code}, safe=False)
            except Exception as e:
                otp_Seriyalizer = OtpSerialiser(
                    otpUser, data={'number': id[2:], 'otp': code})
                if otp_Seriyalizer.is_valid():
                    otp_Seriyalizer.save()
                    return JsonResponse({'Status': True, 'Message': 'OTP sent to your given number +'+id, 'OtpCode': code}, safe=False)
        else:
            return JsonResponse({'Status': False, 'Message': 'Phone number is not valid'}, safe=False)


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
                    return JsonResponse({'Status': True, 'Message': 'Data updated successfully',  'User': user_serializer.data}, safe=False)
                return JsonResponse({'Status': False, 'Message': 'Failed to Update'}, safe=False, status=400)

            else:
                user_serializer = UserSerialiser(
                    user, data={'Name': users_data['Name']})
                if user_serializer.is_valid():
                    user_serializer.save()
                    return JsonResponse({'Status': True, 'Message': 'Data updated successfully'}, safe=False)
                return JsonResponse({'Status': False, 'Message': 'Failed to Update'}, safe=False, status=400)

        elif request.method == 'DELETE':
            user = UserData.objects.get(UserId=id)
            user.delete()
            return JsonResponse({'Status': True, 'Message': 'Data Deleted successfully'}, safe=False)

    except Exception as e:
        er_str = str(e)
        return JsonResponse({'Status': False, 'Message': 'Failed to update', 'Error': er_str}, safe=False, status=400)

import bcrypt
import json
import jwt
import requests

from django.http            import JsonResponse
from django.views           import View

from .models import User
import my_settings

class KakaoSigninView(View):
    def post(self, request):
        try:
            access_token    = request.headers['Authorization']

            profile_request = requests.get(
                    "https://kapi.kakao.com/v2/user/me", 
                    headers={"Authorization" : f"Bearer {access_token}"}
            ).json()

            if profile_request.get('code')==-401 or not profile_request:
                return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 401)

            id_number       = profile_request.get('id')
            email           = profile_request.get('kakao_account').get('email')

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message' : 'INVALID_USER', 'id_number' : id_number, 'email' : email }, status=401)

            token = jwt.encode({
                'user_id':User.objects.filter(email=email).first().id}, 
                my_settings.SECRET_KEY, algorithm="HS256"
            )
            return JsonResponse({'message' : 'SUCCESS', 'token' : token}, status=200)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        
class KakaoSignupView(View):
    def post(self, request):     
        try:
            data = json.loads(request.body)
            email         = data['email']
            id_number     = str(data['id_number'])
            name          = data['name']
            phone_number  = data['phone_number']

            if not my_settings.EMAIL_CHECK.match(email): 
                return JsonResponse({"message" : "EMAIL_ERROR"}, status=400)

            if not my_settings.ID_NUMBER_CHECK.match(id_number): 
                return JsonResponse({"message" : "ID_NUMBER_ERROR"}, status=400)

            if not my_settings.NAME_CHECK.match(name): 
                return JsonResponse({"message" : "NAME_ERROR"}, status=400)

            if not my_settings.PHONE_NUMBER_CHECK.match(phone_number): 
                return JsonResponse({"message" : "PHONE_NUMBER_ERROR"}, status=400)

            hashed_password = bcrypt.hashpw(id_number.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')

            user = User(
                email        = email,
                password     = hashed_password,
                name         = name,
                phone_number = phone_number,
            )
            user.save()

            token = jwt.encode({'user_id': user.id}, my_settings.SECRET_KEY, algorithm="HS256")      
            return JsonResponse({"message" : "SUCCESS", "token" : token}, status = 200)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

        except json.JSONDecodeError:
            return JsonResponse({"message" : "Json_Decode_Error"}, status = 400)
import json
import jwt

from django.http import JsonResponse

from .models import User
import my_settings

def login_required(func):
    def decorator(self, request, *args, **kwargs):
        try:
            encoded_token = request.headers['Authorization']
            decoded_token = jwt.decode(encoded_token, my_settings.SECRET_KEY, algorithms='HS256')

            user = User.objects.get(id=decoded_token['user_id'])   

            request.user = user
            return func(self, request, *args, **kwargs)

        except User.DoesNotExist:
            return JsonResponse({"message":"UNKNOWN_USER"}, status = 401)

        except KeyError:
            return JsonResponse({"message":"INVALID_LOGIN"}, status = 401)

        except jwt.DecodeError:
            return JsonResponse({"message":"INVALID_TOKEN"}, status = 401)

    return decorator
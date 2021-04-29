import bcrypt
import jwt
import json
from unittest.mock import patch, MagicMock

from django.test   import Client, TestCase

from users.models  import User
import my_settings

class KakaoSignInTest(TestCase): 
    def setUp(self):
        password          = '1234'
        hashed_password   = bcrypt.hashpw(
                password.encode('UTF-8'), bcrypt.gensalt()
            ).decode('UTF-8')
        User.objects.create(
            name          = '침착맨',
            email         = 'test@gmail.com',
            password      = hashed_password,
            phone_number  = '01012341111',
           )

    def tearDown(self):
        User.objects.filter(name='침착맨').delete()

    def test_key_error(self):
        c = Client()
        header = {}
        
        response = c.post('/users/kakao-signin', content_type='applications/json', **header)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    "message"   : "KEY_ERROR",
                }
            )

    @patch('users.views.requests') 
    def test_kakao_signin_invalid_token(self, mocked_request):

        class FakeResponse:
            def json(self):
                return {
                }
        
        mocked_request.get = MagicMock(return_value = FakeResponse())
        
        c = Client()
        header = {'HTTP_Authorization':'fake_token.1234'}

        response = c.post('/users/kakao-signin', content_type='applications/json', **header)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
                {
                    "message"   : "INVALID_TOKEN",
                }
            )

    @patch('users.views.requests') 
    def test_kakao_signin_invalid_user(self, mocked_request):

        class FakeResponse:
            def json(self):
                return {
                    "id" : 123456,
                    "kakao_account": {"email":"test@naver.com"}
                }

        mocked_request.get = MagicMock(return_value = FakeResponse())
        
        c = Client()
        header = {'HTTP_Authorization':'fake_token.1234'}
        
        response = c.post('/users/kakao-signin', content_type='applications/json', **header)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
                {
                    "message"   : "INVALID_USER",
                    "id_number" : 123456,
                    "email"     : "test@naver.com",
                }
            )

    @patch('users.views.requests') 
    def test_kakao_signin_success(self, mocked_request):

        class FakeResponse:
            def json(self):
                return {
                    "id" : 123456,
                    "kakao_account": {"email":"test@gmail.com"}
                }
        
        mocked_request.get = MagicMock(return_value = FakeResponse())
        token = jwt.encode({
                'user_id':User.objects.get(email="test@gmail.com").id}, 
                my_settings.SECRET_KEY, algorithm="HS256"
            )

        c = Client()
        header = {'HTTP_Authorization':'fake_token.1234'}
        
        response = c.post('/users/kakao-signin', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {
                    "message" : "SUCCESS",
                    "token"   : token,
                }
            )
if __name__ == '__main__':
    unittest.main()

class KakaoSignupTest(TestCase): 
    def test_email_error(self):
        c = Client()
        params = {
            "email"        : "turkymp3naver.com",
            "id_number"    : 123456,
            "name"         : "주펄린",
            "phone_number" : "01033332222",
        }
        
        response = c.post('/users/kakao-signup', json.dumps(params), content_type='applications/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    "message"   : "EMAIL_ERROR",
                }
            )
    def test_id_number_error(self):
        c = Client()
        params = {
            "email"        : "turkymp3@naver.com",
            "id_number"    : "abcd",
            "name"         : "주펄린",
            "phone_number" : "01033332222",
        }
        
        response = c.post('/users/kakao-signup', json.dumps(params), content_type='applications/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    "message"   : "ID_NUMBER_ERROR",
                }
            )
    def test_name_error(self):
        c = Client()
        params = {
            "email"        : "turkymp3@naver.com",
            "id_number"    : 123456,
            "name"         : "",
            "phone_number" : "01033332222",
        }
        
        response = c.post('/users/kakao-signup', json.dumps(params), content_type='applications/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    "message"   : "NAME_ERROR",
                }
            )
    def test_phone_number_error(self):
        c = Client()
        params = {
            "email"        : "turkymp3@naver.com",
            "id_number"    : 123456,
            "name"         : "주펄린",
            "phone_number" : "0103333",
        }
        
        response = c.post('/users/kakao-signup', json.dumps(params), content_type='applications/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    "message"   : "PHONE_NUMBER_ERROR",
                }
            )

    def test_key_error(self):
        c = Client()
        params = {
            "email"       : "turkymp3@naver.com",
            "id_number"    : 123456,
            "name"         : "주펄린",
        }
        
        response = c.post('/users/kakao-signup', json.dumps(params), content_type='applications/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    "message"   : "KEY_ERROR",
                }
            )

    def test_json_decoder_error(self):
        c = Client()
        params = {
            "email"        : "turkymp3@naver.com",
            "id_number"    : 123456,
            "name"         : "주펄린",
            "phone_number" : "01033333233",
        }
        
        response = c.post('/users/kakao-signup', params, content_type='applications/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    "message"   : "Json_Decode_Error",
                }
            )

    @patch('users.views.requests') 
    def test_kakao_signup_success(self, mocked_request):
        c = Client()
        params = {
            "email"        : "turkymp3@naver.com",
            "id_number"    : 123456,
            "name"         : "주펄린",
            "phone_number" : "01033333233",
        }
        
        response = c.post('/users/kakao-signup', json.dumps(params), content_type='applications/json')
        token = jwt.encode({
                'user_id':User.objects.get(email="turkymp3@naver.com").id}, 
                my_settings.SECRET_KEY, algorithm="HS256"
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {
                    "message"   : "SUCCESS",
                    "token"     : token
                }
            )
if __name__ == '__main__':
    unittest.main()

import json

from haversine     import haversine
from django.test   import TestCase, Client
from unittest.mock import patch, MagicMock, Mock

from .models       import Company, CompanyImage

class CompanyMainViewTest(TestCase):
    
    def setUp(self):
        Company.objects.create(
            id              = 1,
            name            = '위코드',
            address         = '서울특별시 강남구 어딘가',
            star_rating     = 4.7,
            contract_number = 17,
            upper_price     = 17000000,
            lower_price     = 12000000,
            latitude        = 39.123451235,
            longtitude      = 127.123979147,
            thumbnail_image = '내가 섬네일 이미지가 어디있습니까',
        )
        
        CompanyImage.objects.create(
            company_id = 1,
            image_url  = 'dlrjtdmsdlalwlurldlqslekwprlfkf',
        )
        
        CompanyImage.objects.create(
            company_id = 1,
            image_url  = 'dlrjasdfasfdsaflwlurldlqslekwprlfkf',
        )
        
        CompanyImage.objects.create(
            company_id = 1,
            image_url  = 'dlrrwettwreurldlqslekwprlfkf',
        )
        
    def tearDown(self):
        Company.objects.all().delete()
        CompanyImage.objects.all().delete()

    @patch('companies.views.requests')
    def test_company_filter_get_success(self, mock_kakao_requests):
        client = Client()
        
        class MockedResponse:
            def json(self):
                return{
                "documents": [
            {
            "address": {
                    "address_name"        : "서울 강남구 역삼1동",
                    "b_code"              : "",
                    "h_code"              : "1168064000",
                    "main_address_no"     : "",
                    "mountain_yn"         : "N",
                    "region_1depth_name"  : "서울",
                    "region_2depth_name"  : "강남구",
                    "region_3depth_h_name": "역삼1동",
                    "region_3depth_name"  : "",
                    "sub_address_no"      : "",
                    "x"                   : "127.033201083326",
                    "y"                   : "37.4954171091244"
                },
                "address_name": "서울 강남구 역삼1동",
                "address_type": "REGION",
                "road_address": '제발 적당히 좀 해 .......',
                "x"           : "127.033201083326",
                "y"           : "37.4954171091244"
            }
        ],
        "meta": {
            "is_end"        : '다 해줄게 제발 보내줘',
            "pageable_count": 1,
            "total_count"   : 1
}
                }
                
        mock_kakao_requests.get = MagicMock(return_value = MockedResponse())
        
        response = client.get("/companies?location='서울특별시 강남구 어디쯤'&radius=200")
        
        self.assertEqual(response.json(),
        {"MESSAGE": [
            {
            "id"             : 1,
            "name"           : "위코드",
            "address"        : '서울특별시 강남구 어딘가',
            "star_rating"    : "4.70",
            "upper_price"    : "17000000.00",
            "lower_price"    : "12000000.00",
            "distance"       : 181.2,
            "latitude"       : "39.12345123499999743899",
            "longtitude"     : "127.12397914700000001176",
            "contract_number": 17,
            "thumbnail"      : "내가 섬네일 이미지가 어디있습니까",
            "images"         : 
            [
                'dlrjtdmsdlalwlurldlqslekwprlfkf',
                'dlrjasdfasfdsaflwlurldlqslekwprlfkf',
                'dlrrwettwreurldlqslekwprlfkf',
            ]
        }]})
        self.assertEqual(response.status_code, 200)

    @patch('companies.views.requests')
    def test_company_default_value_get_success(self, mock_kakao_requests):
        client = Client()
        
        class MockedResponse:
            def json(self):
                return{
                "documents": [
            {
            "address": {
                    "address_name"        : "서울 강남구 역삼1동",
                    "b_code"              : "",
                    "h_code"              : "1168064000",
                    "main_address_no"     : "",
                    "mountain_yn"         : "N",
                    "region_1depth_name"  : "서울",
                    "region_2depth_name"  : "강남구",
                    "region_3depth_h_name": "역삼1동",
                    "region_3depth_name"  : "",
                    "sub_address_no"      : "",
                    "x"                   : "127.033201083326",
                    "y"                   : "37.4954171091244"
                },
                "address_name": "서울 강남구 역삼1동",
                "address_type": "REGION",
                "road_address": '제발 적당히 좀 해 .......',
                "x"           : "127.033201083326",
                "y"           : "37.4954171091244"
            }
        ],
        "meta": {
            "is_end"        : '다 해줄게 제발 보내줘',
            "pageable_count": 1,
            "total_count"   : 1
}
                }
                
        mock_kakao_requests.get = MagicMock(return_value = MockedResponse())
        
        response = client.get("/companies?location='서울특별시 강남구 어디쯤'")
        DEF_RADIUS = 5.0
        
        self.assertEqual(response.json(),
        {'MESSAGE': []})
        self.assertEqual(response.status_code, 200)

import json
import boto3
import jwt
import unittest

from unittest.mock import patch, MagicMock

from django.test        import TestCase, Client
from django.core.files  import File

from products.models  import Category, Product, Review, Size, Color, ProductOption, ProductImage
from users.models     import User

from my_settings import SECRET_KEY

class CategoryViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='침',image_url='https://un.com')
        Category.objects.create(name='주',image_url='https://us.com')
        Category.objects.create(name='아',image_url='https://ns.com')

    def tearDown(self):
        Category.objects.all().delete()
    
    def test_category_view_test(self):
        client = Client()
        response = client.get('/store/category')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
        {'MESSAGE': 'SUCCESS', 
        'category_lists': [
            {'category_id': 1, 'name': '침', 'image_url': 'https://un.com'},
            {'category_id': 2, 'name': '주', 'image_url': 'https://us.com'},
            {'category_id': 3, 'name': '아', 'image_url': 'https://ns.com'}
            ]}
            )
class ProductListView(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        a  = Category.objects.create(id=1,name='침',image_url='https://un.com')
        b  = Category.objects.create(id=2,name='주',image_url='https://us.com')
        c  = Category.objects.create(id=3,name='아',image_url='https://ns.com')
        p1 = Product.objects.create(id=1,name='가1',price=1100,discount_rate=0.1,
            is_freedelivery=True,delivery_fee=500,delivery_method=True,thumbnail_image='https://ima.com',
            category=a,manufacturer='소',description='a',description_image='https://ima.com')
        p2 = Product.objects.create(id=2,name='가2',price=1200,discount_rate=0.2,
            is_freedelivery=False,delivery_fee=500,delivery_method=True,thumbnail_image='https://ima.com',
            category=b,manufacturer='sf',description='a',description_image='https://ima.com')
        p3 = Product.objects.create(id=3,name='가3',price=1300,discount_rate=0.3,
            is_freedelivery=True,delivery_fee=500,delivery_method=True,thumbnail_image='https://ima.com',
            category=b,manufacturer='f',description='란',description_image='https://ima')
        p4 = Product.objects.create(id=4,name='가4',price=1400,discount_rate=0.4,
            is_freedelivery=False,delivery_fee=500,delivery_method=True,thumbnail_image='https://ima.com',
            category=c,manufacturer='f',description='찬f',description_image='https://ima.com')
        u1 = User.objects.create(id=1,name='1',email='fda@naver.com',
            password='fjd',phone_number='010-1234-5611')
        u2 = User.objects.create(id=2,name='2',email='fda@naver.com',
            password='fj',phone_number='010-1234-5611')
        u3 = User.objects.create(id=3,name='3',email='fda@naver.com',
            password='fkf',phone_number='010-1234-5611')
        u4 = User.objects.create(id=4,name='4',email='fda@naver.com',
            password='fjf',phone_number='010-1234-5611')
        u5 = User.objects.create(id=5,name='5',email='fda@naver.com',
            password='kf',phone_number='010-1234-5611')
        Review.objects.create(user=u1,product=p1,star_rating=5,image_url='https://ima.com',text='fd')
        Review.objects.create(user=u2,product=p1,star_rating=1,image_url='https://ima.com',text='fd')
        Review.objects.create(user=u3,product=p1,star_rating=1,image_url='https://ima.com',text='fd')
        Review.objects.create(user=u5,product=p1,star_rating=2,image_url='https://ima.com',text='fd')
        Review.objects.create(user=u2,product=p2,star_rating=3,image_url='https://ima.com',text='fd')
        Review.objects.create(user=u4,product=p2,star_rating=4,image_url='https://ima.com',text='fd')
        Review.objects.create(user=u3,product=p2,star_rating=1,image_url='https://ima.com',text='fd')
        Review.objects.create(user=u1,product=p2,star_rating=3,image_url='https://ima.com',text='fd')
        Review.objects.create(user=u1,product=p3,star_rating=2,image_url='https://ima.com',text='fd')
        Review.objects.create(user=u2,product=p3,star_rating=2,image_url='https://ima.com',text='fd')
        Review.objects.create(user=u3,product=p3,star_rating=2,image_url='https://ima.com',text='fd')
        Review.objects.create(user=u4,product=p3,star_rating=2,image_url='https://ima.com',text='fd')
        Review.objects.create(user=u5,product=p4,star_rating=4,image_url='https://ima.com',text='fd')
        Review.objects.create(user=u4,product=p4,star_rating=3,image_url='https://ima.com',text='fd')
        Review.objects.create(user=u3,product=p4,star_rating=3,image_url='https://ima.com',text='fd')
        Review.objects.create(user=u2,product=p4,star_rating=3,image_url='https://ima.com',text='fd')
    
    def tearDown(self):
        Category.objects.all().delete()
        User.objects.all().delete()
        Product.objects.all().delete()
        Review.objects.all().delete()
    
    def test_product_list_view_(self):
        client=Client()
        response = client.get('/store')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'MESSAGE': 'SUCCESS',
            'product_lists': [
                {'id': 4, 'name': '가4', 'price': '1400.00',
                    'manufacturer': 'f', 'discount_rate': '0.40',
                    'star_rating': '3.2', 'review_number': 4, 'is_freedelivery': False,
                    'thumbnail_image': 'https://ima.com'},
                {'id': 3, 'name': '가3', 'price': '1300.00',
                    'manufacturer': 'f', 'discount_rate': '0.30',
                    'star_rating': '2.0', 'review_number': 4, 'is_freedelivery': True,
                    'thumbnail_image': 'https://ima.com'},
                {'id': 2, 'name': '가2', 'price': '1200.00',
                    'manufacturer': 'sf', 'discount_rate': '0.20',
                    'star_rating': '2.8', 'review_number': 4, 'is_freedelivery': False,
                    'thumbnail_image': 'https://ima.com'},
                {'id': 1, 'name': '가1', 'price': '1100.00',
                    'manufacturer': '소', 'discount_rate': '0.10',
                    'star_rating': '2.2', 'review_number': 4, 'is_freedelivery': True,
                    'thumbnail_image': 'https://ima.com'}]})
        
    def test_invalid_category_id(self):
        client=Client()
        response = client.get('/store?category-id=5')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{'MESSAGE': 'INVALID_CATEGORY_ID'})
    
    def test_ordering_value_error(self):
        client=Client()
        response = client.get('/store?ordering=33')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{'MESSAGE': 'INVALID_ORDERING_METHOD'})

class ProductDetailViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        a  = Category.objects.create(id=1,name='침실/가구',image_url='https://ima.com')
        p1 = Product.objects.create(id=1,name='가구1',price=1100,discount_rate=0.1,is_freedelivery=True,
            delivery_fee=500,delivery_method=True,thumbnail_image='https://ima.com',category=a,
            manufacturer='다이소',description='aaaa',description_image='https://ima.com')
        s1 = Size.objects.create(name='small')
        s2 = Size.objects.create(name='large')
        c1 = Color.objects.create(name='red')
        c2 = Color.objects.create(name='blue')
        ProductOption.objects.create(product=p1,size=s1,color=c1)
        ProductOption.objects.create(product=p1,size=s2,color=c2)
        ProductImage.objects.create(product=p1,image_url='https://ima.com')
        ProductImage.objects.create(product=p1,image_url='https://im.com')
        u1 = User.objects.create(id=1,name='1',email='fda@naver.com',password='fjd',phone_number='010-1234-4567')
        u2 = User.objects.create(id=2,name='2',email='fda@naver.com',password='fkf',phone_number='010-1234-4567')
        u3 = User.objects.create(id=3,name='3',email='fda@naver.com',password='lkf',phone_number='010-1234-4567')
        Review.objects.create(user=u1,product=p1,star_rating=5,image_url='https://i.com',text='fd')
        Review.objects.create(user=u2,product=p1,star_rating=1,image_url='https://im.com',text='fd')
        Review.objects.create(user=u3,product=p1,star_rating=1,image_url='https://imag',text='fd')


    def tearDown(self):
        Category.objects.all().delete()
        Product.objects.all().delete()
        Size.objects.all().delete()
        Color.objects.all().delete()
        Review.objects.all().delete()
        User.objects.all().delete()
    
    def test_product_detail_view(self):
        client=Client()
        response = client.get('/store/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'MESSAGE': 'SUCCESS',
            'product_info': {
                'category': '침실/가구',
                'manufacturer': '다이소',
                'name': '가구1',
                'star_rating': '2.333333',
                'review_number': 3,
                'price': '1100.00',
                'discout_rate': '0.10',
                'delivery_fee': '500.00',
                'delivery_method': True,
                'size': ['small', 'large'],
                'color': ['red', 'blue'],
                'thumbnail_image': 'https://ima.com',
                'description': 'aaaa',
                'description_image': 'https://ima.com',
                'product_images': ['https://ima.com', 'https://im.com']}})
        
    def test_invalid_product_id(self):
        client=Client()
        response = client.get('/store/4')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'MESSAGE': 'PRODUCT_ID_DOES_NOT_EXISTS'})

class ProductReviewTest(TestCase):

    def setUp(self):
        a  = Category.objects.create(id=1,name='침실/가구',image_url='https://ima.com')
        p1 = Product.objects.create(id=1,name='가구1',price=1100,discount_rate=0.1,is_freedelivery=True,
            delivery_fee=500,delivery_method=True,thumbnail_image='https://ima.com',category=a,
            manufacturer='다이소',description='aaaa',description_image='https://ima.com')
        Product.objects.create(id=2,name='가4',price=1400,discount_rate=0.4,
            is_freedelivery=False,delivery_fee=500,delivery_method=True,thumbnail_image='https://ima.com',
            category_id=1,manufacturer='f',description='찬f',description_image='https://ima.com')
        u1 = User.objects.create(id=1,name='1',email='fda@naver.com',password='fjd',phone_number='010-1234-4567')
        Review.objects.create(user=u1,product=p1,star_rating=5,image_url='https://i.com',text='fd')

    def tearDown(self):
        Category.objects.all().delete()
        Product.objects.all().delete()
        Review.objects.all().delete()

    @patch('products.views.boto3.client')
    def test_review_upload(self, mock_s3client):
        client                       = Client()
        mock_file                    = MagicMock(spec=File)
        mock_file.name               = '101.jpg'
        mock_s3client.upload_fileobj = MagicMock()
        access_token                 = jwt.encode({'user_id': 1}, SECRET_KEY, algorithm='HS256')
        headers                      = {'HTTP_Authorization': access_token}
        form_data                    = {'filename': mock_file,'json':json.dumps({'star_rating':3,'text':'aa'})}
        response = client.post('/store/review/1', form_data, **headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'MESSAGE': 'SUCCESS'})

    def test_review_show(self):
        client=Client()
        response = client.get('/store/review/1')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'MESSAGE': 'SUCCESS',
            'Review_lists': [
                {'user': '1',
                    'star_rating': '5.00',
                    'text': 'fd',
                    'image_url': 'https://i.com'}]
                    })
    
    def test_review_invalid_product(self):
        client = Client()
        response = client.get('/store/review/5')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{'MESSAGE':'INVALID_PRODUCT_ID'})
from django.test import TestCase, Client
from products.models import Category, Product, Review
from users.models import User

import json


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
                 'thumbnail_image': 'https://ima.com'}]
                 })
        
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

import json
import boto3
import random
import my_settings

from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q, Avg
from django.core.exceptions import FieldError, ObjectDoesNotExist

from products.models  import Product, Category, Review
from users.decorators import login_required

class CategoryView(View):
    def get(self,request):
        category_lists = [
            {
            'category_id' : category.id,
            'name'        : category.name,
            'image_url'   : category.image_url
            }
        for category in Category.objects.all()]        
        return JsonResponse({'MESSAGE':'SUCCESS','category_lists':category_lists}, status=200)

class ProductListView(View):
    def get(self,request):
        try: 
            ordering    = request.GET.get('ordering','-price')
            category_id = request.GET.get('category-id', None)

            q=Q()
            if category_id:
                q = Q(category_id=category_id)
            products = Product.objects.filter(q).annotate(star_rating=Avg('review__star_rating')).order_by(ordering)
            
            product_lists = [
                {
                    'id'                  : product.id,
                    'name'                : product.name,
                    'price'               : product.price,
                    'manufacturer'        : product.manufacturer,
                    'discount_rate'       : product.discount_rate,
                    'star_rating'         : round(product.review_set.all().aggregate(Avg('star_rating'))['star_rating__avg'],1) if product.review_set.all() else None,
                    'review_number'       : product.review_set.count(),
                    'is_freedelivery'     : product.is_freedelivery,
                    'thumbnail_image'     : product.thumbnail_image,
                    'hot_deal'            : random.randrange(0,2), 
                } for product in products]
            
            if len(product_lists)==0:
                return JsonResponse({'MESSAGE':'INVALID_CATEGORY_ID'}, status=401)
            
            return JsonResponse({'MESSAGE':'SUCCESS','product_lists':product_lists}, status=200)
        except FieldError:
            return JsonResponse({'MESSAGE':'INVALID_ORDERING_METHOD'}, status=401)

class ProductDetailView(View):
    def get(self,request,product_id):
        try:
            product = Product.objects.select_related('category').prefetch_related(
                'review_set','size','color','productimage_set').get(id=product_id)
            product_info = {
                'category'          : product.category.name,
                'manufacturer'      : product.manufacturer,
                'name'              : product.name,
                'star_rating'       : product.review_set.all().aggregate(Avg('star_rating')).get('star_rating__avg', None) if product.review_set.all() else None,
                'review_number'     : product.review_set.count(),
                'price'             : product.price,
                'discout_rate'      : product.discount_rate,
                'delivery_fee'      : product.delivery_fee,
                'delivery_method'   : product.delivery_method,
                'size'              : list(set([size.name for size in product.size.all()])),
                'color'             : list(set([color.name for color in product.color.all()])),
                'thumbnail_image'   : product.thumbnail_image,
                'description'       : product.description,
                'description_image' : product.description_image,
                'product_images'    : [image.image_url for image in product.productimage_set.all()]
                }
            return JsonResponse({'MESSAGE':'SUCCESS','product_info':product_info}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':'PRODUCT_ID_DOES_NOT_EXISTS'}, status=401)

class ProductReviewView(View):
    
    @login_required
    def post(self, request, product_id):
        data        = json.loads(request.POST.get('json'))
        file        = request.FILES.get('filename')
        star_rating = data.get('star_rating')
        text        = data.get('text')
        
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id = my_settings.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key = my_settings.AWS_S3_SECRET_ACCESS_KEY
        )
        
        self.s3_client.upload_fileobj(
            file, 
            my_settings.AWS_STORAGE_BUCKET_NAME,
            file.name,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )
        if file:
            file_endpoint = str(file.name).replace(' ','+')
            image_url     = f'https://herhousebucket.s3.ap-northeast-2.amazonaws.com/{file_endpoint}'
        
        Review.objects.create(star_rating  = star_rating,
                                text       = text,
                                product_id = product_id,
                                user_id    = request.user.id,
                                image_url  = image_url if file else None)

        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

    def get(self, request, product_id):
        try:
            product = Product.objects.prefetch_related('review_set','user').get(id = product_id)
            review_lists = [{
                'user' : review.user.name,
                'star_rating' : review.star_rating,
                'text' : review.text,
                'image_url' : review.image_url} for review in product.review_set.all()] if product.review_set.all() else None     
            return JsonResponse({'MESSAGE':'SUCCESS', 'Review_lists': review_lists}, status=201)
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_PRODUCT_ID'}, status=401)
import json

from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q, Avg
from django.core.exceptions import FieldError

from products.models import Category, Product

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
            
            if len(products)==0:
                return JsonResponse({'MESSAGE':'INVALID_CATEGORY_ID'}, status=401)
            
            product_lists = [
                {
                    'id'              : product.id,
                    'name'            : product.name,
                    'price'           : product.price,
                    'manufacturer'    : product.manufacturer,
                    'discount_rate'   : product.discount_rate,
                    'star_rating'     : round(product.review_set.all().aggregate(Avg('star_rating'))['star_rating__avg'],1),
                    'review_number'   : product.review_set.count(),
                    'is_freedelivery' : product.is_freedelivery,
                    'thumbnail_image' : product.thumbnail_image
                } for product in products]
            
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
                'star_rating'       : product.review_set.all().aggregate(Avg('star_rating')).get('star_rating__avg', None),
                'review_number'     : product.review_set.count(),
                'discout_rate'      : product.discount_rate,
                'delivery_fee'      : product.delivery_fee,
                'delivery_method'   : product.delivery_method,
                'size'              : [size.name for size in product.size.all()],
                'color'             : [color.name for color in product.color.all()],
                'thumbnail_image'   : product.thumbnail_image,
                'description'       : product.description,
                'description_image' : product.description_image,
                'product_images'    : [image.image_url for image in product.productimage_set.all()]
                }
            return JsonResponse({'MESSAGE':'SUCCESS','product_info':product_info}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':'PRODUCT_ID_DOES_NOT_EXISTS'}, status=401)
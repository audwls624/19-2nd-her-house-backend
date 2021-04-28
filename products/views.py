import json

from django.http  import JsonResponse
from django.views import View

from products.models import Category

class CategoryView(View):
    def get(self,request):
        category_lists = [
            {
            category_id : category.id,
            name        : category.name,
            image_url   : category.image_url
            }
        for category in Category.objects.all()]        
        return JsonResponse({'MESSAGE':'SUCCESS','category_lists':category_lists}, status=200)
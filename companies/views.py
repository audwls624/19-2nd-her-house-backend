import json
import requests

from haversine    import haversine
from urllib.parse import urlparse

from django.http  import JsonResponse
from django.views import View

from .models      import Company, CompanyImage
from my_settings  import API_KEY

class CompanyMainView(View):
    def get(self, request):
        location   = request.GET.get('location', None)
        DEF_RADIUS = 5.0
        radius     = request.GET.get('radius', DEF_RADIUS)

        if location:
            url      = 'https://dapi.kakao.com/v2/local/search/address.json?&query=' + location
            result   = requests.get(urlparse(url).geturl(), headers={'Authorization': f'KakaoAK {API_KEY}'}).json()
            match    = result['documents'][0]['address']
            user_lat = float(match['y'])
            user_lng = float(match['x'])

        user_location = (user_lat, user_lng)
        
        company = [{
            'id'               : company.id,
            'name'             : company.name,
            'address'          : company.address,
            'star_rating'      : company.star_rating,
            'upper_price'      : company.upper_price,
            'lower_price'      : company.lower_price,
            'distance'         : round(haversine((company.latitude, company.longtitude), user_location), 1),
            'contract_number'  : company.contract_number,
            'thumbnail'        : company.thumbnail_image,
            'images'           : [i.image_url for i in company.companyimage_set.all()]}
            for company in Company.objects.all().prefetch_related('companyimage_set')]
        
        company = [x for x in company if x['distance'] <= float(radius)]

        return JsonResponse({'MESSAGE':company}, status=200)

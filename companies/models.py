from django.db import models

class Company(models.Model):
    name               = models.CharField(max_length=45)
    address            = models.CharField(max_length=100)
    star_rating        = models.DecimalField(max_digits=3, decimal_places=2)
    contract_number    = models.IntegerField()
    upper_price        = models.DecimalField(max_digits=10, decimal_places=2)
    lower_price        = models.DecimalField(max_digits=10, decimal_places=2)
    latitude           = models.DecimalField(max_digits=25, decimal_places=20)
    longtitude         = models.DecimalField(max_digits=25, decimal_places=20)
    thumbnail_image    = models.URLField(max_length=2000)

    class Meta:
        db_table = 'companies'

class CompanyImage(models.Model):
    company   = models.ForeignKey('Company', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'company_images'

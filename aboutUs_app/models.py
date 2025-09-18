from django.db import models

# Create your models here.
class Setup_page(models.Model):
    brand_name = models.CharField(max_length=200)
    brand_logo = models.ImageField(upload_to='logo/')
    welcome_text = models.TextField()

class SliderBanners(models.Model):
    image = models.ImageField(upload_to='banners/')
    name = models.CharField(max_length=200)

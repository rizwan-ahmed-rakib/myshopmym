from django.db import models

# Create your models here.

"""product category model"""


class Category(models.Model):
    title = models.CharField(max_length=20)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        blank=True,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='categories', blank=True)
    brand_image = models.ImageField(upload_to='brand', blank=True,null=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"

    """product model"""


class Product(models.Model):
    mainimage = models.ImageField(upload_to='products/')
    image1 = models.ImageField(upload_to='products/',blank=True,null=True)
    image2 = models.ImageField(upload_to='products/',blank=True,null=True)
    image3 = models.ImageField(upload_to='products/',blank=True,null=True)
    name = models.CharField(max_length=264)
    product_code = models.CharField(max_length=20,default='ABC123')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Category')
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text')
    detail_text = models.TextField(max_length=1000, verbose_name='Description')
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    stock_status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', ]
        # here -created mentions that it will show the latest product top

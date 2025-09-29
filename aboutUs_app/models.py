from django.db import models

# Create your models here.
class Setup_page(models.Model):
    brand_name = models.CharField(max_length=200)
    brand_logo = models.ImageField(upload_to='logo/')
    welcome_text = models.TextField()

class SliderBanners(models.Model):
    image = models.ImageField(upload_to='banners/')
    name = models.CharField(max_length=200)





class ContactInfo(models.Model):
    address = models.TextField()
    phone_primary = models.CharField(max_length=20)
    phone_secondary = models.CharField(max_length=20, blank=True, null=True)
    email_primary = models.EmailField()
    email_secondary = models.EmailField(blank=True, null=True)
    business_hours_weekdays = models.CharField(max_length=100, default="Mon-Fri: 9AM - 8PM")
    business_hours_weekend = models.CharField(max_length=100, default="Sat-Sun: 10AM - 6PM")

    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Contact Info ({self.id})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

from django.db import models
# to create a customer user model and adnin panel
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy

# to autometically create one to one objects
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.+

# class MyUserManager(BaseUserManager):  # for handling user
#     """a custom manager to deak with emails as unique identifoer"""
#
#     def _create_user(self, email, password, **extra_fields):  # for use email and password for creatong user
#         """""create and save a user with a given enail and password"""
#
#         if not email:
#             raise ValueError("the email must be set")
#
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", False)
#         extra_fields.setdefault("is_superuser", False)
#         return self._create_user(email, password, **extra_fields)
#
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is staff')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is superuser=True')
#         return self._create_user(email, password, **extra_fields)


class MyUserManager(BaseUserManager):
    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError("The phone number must be set")

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True, null=False)  # 📌 Email বাদ দিয়ে Phone unique করো
    email = models.EmailField(blank=True, null=True)  # চাইলে optional রাখো
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "phone"  # 📌 এখন phone হবে login identifier
    REQUIRED_FIELDS = []      # superuser বানানোর সময় আর কিছু লাগবে না

    objects = MyUserManager()

    def __str__(self):
        return self.phone


# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True, null=False)
#     is_staff = models.BooleanField(
#         gettext_lazy('staff status'),  #
#         default=False,
#         help_text=gettext_lazy('desegnet whether the user can login this site')  # )
#     )
#     is_active = models.BooleanField(
#         gettext_lazy('active'),  #
#         default=True,
#         help_text=gettext_lazy(
#             'desegnation wheather this user should be terated as active.unselect this instead of deleting accounts')
#         # '
#         # '
#     )
#     USERNAME_FIELD = 'email'
#     objects = MyUserManager()
#
#     def __str__(self):
#         return self.email
#
#     def get_full_name(self):
#         return self.email
#
#     def get_short_name(self):
#         return self.email





class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profilePicture/', blank=True)
    """hwre we have created one to one model relationship with User & Profile"""
    username = models.CharField(max_length=264, blank=True)
    full_name = models.CharField(max_length=264, blank=True)
    address_1 = models.TextField(max_length=300, blank=True)
    city = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    date_joined = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username + "'s profile"

    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]
        for field_name in fields_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()  # if any change goes on User model then effect goes on Profile model,related_name=profile

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# from django.core.files.base import ContentFile
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.files.storage import default_storage
# from PIL import Image
# import io
#
#
# # ✅ কাস্টম ইউজার ম্যানেজার (ইউজার তৈরির নিয়ম নির্ধারণ)
# class MyUserManager(BaseUserManager):
#     def create_user(self, phone_number, password=None, fingerprint_id=None, **extra_fields):
#         if not phone_number:
#             raise ValueError("ফোন নম্বর প্রদান করা আবশ্যক!")
#         user = self.model(phone_number=phone_number, **extra_fields)
#         user.set_password(password)
#         # user.set_password(fingerprint_id)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, phone_number, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(phone_number, password, **extra_fields)
#
#
# # ✅ কাস্টম ইউজার মডেল
# class User(AbstractBaseUser, PermissionsMixin):
#     phone_number = models.CharField(max_length=15, unique=True, verbose_name="ফোন নম্বর")
#     password = models.CharField(max_length=255, null=True, blank=True)
#     fingerprint_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="ফিঙ্গারপ্রিন্ট আইডি")
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#
#     objects = MyUserManager()
#
#     USERNAME_FIELD = 'phone_number'
#     REQUIRED_FIELDS = []
#
#     def __str__(self):
#         return self.phone_number
#
#
# # ✅ Profile Model (ব্যক্তিগত তথ্য সংরক্ষণ করবে)
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     name = models.CharField(max_length=255)
#     email = models.EmailField(null=False, blank=False, default="<EMAIL>")
#     phone_number = models.CharField(max_length=15, blank=True)
#     address = models.CharField(max_length=500, blank=True, verbose_name="ঠিকানা")
#     profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True,
#                                         verbose_name="প্রোফাইল ছবি")
#     city = models.CharField(max_length=50, blank=True)
#
#     zipcode = models.CharField(max_length=10, blank=True)
#     country = models.CharField(max_length=50, blank=True)
#     date_joined = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         # return f"{self.user.phone_number} এর প্রোফাইল"
#         return f"{self.name} এর প্রোফাইল"
#
#     # ✅ Profile Picture সংরক্ষণের আগে ৫০KB-তে কম্প্রেস করা হবে
#     def save(self, *args, **kwargs):
#         if self.profile_picture:
#             img = Image.open(self.profile_picture)
#             output_size = (300, 300)  # ছবির আকার ঠিক করা
#             img.thumbnail(output_size)
#
#             # ✅ ৫০KB-তে কম্প্রেস করা
#             output = io.BytesIO()
#             img.save(output, format='JPEG', quality=50, optimize=True)
#             output.seek(0)
#
#             # 🔹 ফাইল স্টোর করার জন্য ইউজারের আলাদা ফোল্ডার তৈরি
#             folder_path = f'profile_pictures/{self.user.phone_number}/'
#             file_name = f'{folder_path}profile.jpg'
#
#             # ✅ পূর্বের ছবি মুছে ফেলার আগে ফাইল ক্লোজ করে দাও
#             if self.profile_picture.name:
#                 try:
#                     default_storage.delete(self.profile_picture.name)
#                 except PermissionError:
#                     print(f"PermissionError: Could not delete {self.profile_picture.name}")
#
#                 # ✅ `BytesIO` ➝ `ContentFile` (Django-তে ফাইল হিসাবে সংরক্ষণ করতে)
#             image_file = ContentFile(output.getvalue(), name=file_name)
#
#             # ✅ নতুন ছবি সংরক্ষণ
#             self.profile_picture.save(file_name, image_file, save=False)
#
#         super().save(*args, **kwargs)
#
#
# # ✅ User তৈরি হলে স্বয়ংক্রিয়ভাবে Profile তৈরি হবে
# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance, phone_number=instance.phone_number)
#
#
# # ✅ User আপডেট হলে Profile সংরক্ষিত থাকবে
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()

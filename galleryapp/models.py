from django.contrib.auth.models import AbstractUser
from django.db import models

from galleryapp.manager import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    username = None
    mobile_number = models.CharField(max_length=11, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    encrypted_email = models.TextField()
    encrypted_mobile = models.TextField()
    encrypted_password = models.TextField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_number']

    objects = CustomUserManager()


class Album(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='albums/')
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    premium_access_required = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

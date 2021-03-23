from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import datetime


class Countrie(models.Model):
    code = models.CharField(max_length=2, blank=False, primary_key=True)
    name = models.CharField(max_length=50, null=True, blank=False)

    def __str__(self):
        return self.name


class Region(models.Model):
    code = models.IntegerField(blank=False, primary_key=True)
    name = models.CharField(max_length=50, null=True, blank=False)
    country = models.ForeignKey(Countrie, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Citie(models.Model):
    code = models.IntegerField(blank=False, primary_key=True)
    name = models.CharField(max_length=50, null=True, blank=False)
    country = models.ForeignKey(Countrie, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=False)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    country = models.ForeignKey(Countrie, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(Citie, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True, blank=False)
    phone_number = models.CharField(max_length=13, null=True, blank=False)

    def __str__(self):
        return self.user.username


class Categorie(models.Model):
    name = models.CharField(max_length=60, null=True, blank=False)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=60, null=True, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=False)
    price = models.IntegerField(default=10, null=True, blank=False)
    description = models.TextField(null=True, blank=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title


class Picture(models.Model):
    upload_directory = settings.UPLOAD_FOLDER
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def generate_filename(self, filename):
        self.upload_directory = f"{settings.UPLOAD_FOLDER}{self.product.id}/{datetime.timezone.now().microsecond}_{filename}"
        return self.upload_directory

    picture_1 = models.ImageField(upload_to=generate_filename, null=True, blank=True)
    picture_2 = models.ImageField(upload_to=generate_filename, null=True, blank=True)
    picture_3 = models.ImageField(upload_to=generate_filename, null=True, blank=True)

    def __str__(self):
        return self.product.title


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title

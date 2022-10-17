from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    catName = models.CharField(max_length=50)

    def __str__(self):
        return self.catName

class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class Listing(models.Model):
    title = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    description = models.CharField(max_length=1000)
    url = models.CharField(max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="placebid")
    is_active = models.BooleanField(default=False, blank=True, null=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watch_listing")

    def __str__(self):
        return self.title

class Comments(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="comments_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="comments_listing")
    text = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.writer} comment on {self.listing}"
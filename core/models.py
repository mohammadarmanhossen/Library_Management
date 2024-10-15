from django.db import models
from accounts.models import UserAccountModel
from django.contrib.auth.models import User
from .constants import Rating


# Create your models here.
class Deposit(models.Model):
    account = models.ForeignKey(UserAccountModel, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null = True)

    def __str__(self):
        return self.account.user.username
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name
     
class Book(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/')
    category = models.ManyToManyField(Category, related_name='books')
    borrowing_price = models.IntegerField()
    available_copies = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    
class RatingModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    rate = models.CharField(choices=Rating, max_length=100)

    def __str__(self):
        return self.rate


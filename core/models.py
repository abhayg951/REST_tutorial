from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=100)
    publish_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=200)
    description = models.CharField(max_length=200)
    author = models.ForeignKey(User ,on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    
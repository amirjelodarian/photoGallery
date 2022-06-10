from django.db import models

from user.models import User
from category.models import Category

# Create your models here.
class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    path = models.ImageField(upload_to='media/')
    category = models.ManyToManyField(Category)

    def __str__(self):
        self.title
        self.description

    def __unicode__(self):
        self.path


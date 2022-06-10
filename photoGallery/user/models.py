from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        self.name
        self.password
        self.email

    def __unicode__(self):
        self.email

from django.db import models

class Product(models.Model):
    gtin = models.TextField()
    date = models.DateField()

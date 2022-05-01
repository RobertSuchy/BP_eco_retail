from django.db import models

class User(models.Model):
    email = models.CharField(max_length=255)
    


class Product(models.Model):
    name = models.CharField(max_length=255)
    rating = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'products'

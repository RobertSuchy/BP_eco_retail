from django.db import models

# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'products'

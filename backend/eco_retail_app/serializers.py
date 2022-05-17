from rest_framework import serializers
from .models import Product, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'user_type', 'wallet']


class ProductSerializer(serializers.ModelSerializer):
    producer_name = serializers.CharField(source='producer.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'producer_name', 'description', 'rating']

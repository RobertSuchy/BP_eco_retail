from rest_framework import serializers
from .models import Product, RewardsPolicy, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'user_type', 'wallet']


class ProductSerializer(serializers.ModelSerializer):
    producer_name = serializers.CharField(source='producer.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'producer_name', 'description', 'rating']


class RewardsPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardsPolicy
        fields = ['category_a', 'category_b', 'category_c', 'category_d', 'category_e', 'category_f']

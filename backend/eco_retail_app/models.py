from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomAccountManager(BaseUserManager):
    def create_user(self, email, user_type, wallet, password, **other_fields):
        if not email:
            raise ValueError('Email is required')

        if not user_type:
            raise ValueError('User type is required')

        if not wallet:
            raise ValueError('Wallet is required')

        if not password:
            raise ValueError('Password is required')                    

        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, wallet=wallet, **other_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser):
    email = models.CharField(max_length=255, unique=True)

    CUSTOMER = 'customer'
    CHAIN_STORE = 'chain_store'
    PRODUCER = 'producer'

    USER_TYPES = (
        (CUSTOMER, CUSTOMER),
        (CHAIN_STORE, CHAIN_STORE),
        (PRODUCER, PRODUCER)
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPES, default=CUSTOMER)
    wallet = models.CharField(max_length=60)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type', 'wallet']

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'


class Product(models.Model):
    name = models.CharField(max_length=255)
    rating = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'products'

from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, user_type, name, wallet, password, **other_fields):
        if not email:
            raise ValueError('Email is required')

        if not user_type:
            raise ValueError('User type is required')

        if not wallet:
            raise ValueError('Wallet is required')

        if not password:
            raise ValueError('Password is required')                    

        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, name=name, wallet=wallet, **other_fields)
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
    name = models.CharField(max_length=255)
    wallet = models.CharField(max_length=60, unique=True)
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
    producer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=255)

    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'

    ECO_RATING_CATEGORIES = (
        (A, A),
        (B, B),
        (C, C),
        (D, D),
        (E, E),
        (F, F)
    )

    rating = models.CharField(max_length=1, choices=ECO_RATING_CATEGORIES, default=C)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'producer'], name='unique_product')
        ]
        db_table = 'products'


class RewardsPolicy(models.Model):
    chain_store = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    category_a = models.FloatField()
    category_b = models.FloatField()
    category_c = models.FloatField()
    category_d = models.FloatField()
    category_e = models.FloatField()
    category_f = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'rewards_policies'

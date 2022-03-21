from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from json import loads
from .models import *

# Create your views here.

@csrf_exempt
def process_products(request):
    input_body = loads(request.body)
    print(input_body['customer_wallet'])
    reward = 0
    for item in input_body['products']:
        reward += Products.objects.get(id=item['id']).rating * item['price'] * item['amount'] * 1000
    print(reward)
    return HttpResponse(status=200)
    

@csrf_exempt
def add_product(request):
    input_body = loads(request.body)
    
    return HttpResponse(status=200)
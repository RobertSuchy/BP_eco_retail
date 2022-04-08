from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from json import loads
from .models import *
from base64 import b64decode
from typing import Tuple
from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from algosdk import account
from pyteal import compileTeal, Mode, Expr
# from .smart_contract import approval_program, clear_state_program

# Create your views here.

# APPROVAL_PROGRAM = b""
# CLEAR_STATE_PROGRAM = b""

# def compile_contract(client: AlgodClient, contract: Expr) -> bytes:
#     teal = compileTeal(contract, mode=Mode.Application, version=6)
#     response = client.compile(teal)
#     return b64decode(response["result"])


# def get_smart_contract(client: AlgodClient) -> Tuple[bytes, bytes]:
#     global APPROVAL_PROGRAM
#     global CLEAR_STATE_PROGRAM


#     if len(APPROVAL_PROGRAM) == 0:
#         APPROVAL_PROGRAM = compile_contract(client, approval_program())
#         CLEAR_STATE_PROGRAM = compile_contract(client, clear_state_program())

#     return APPROVAL_PROGRAM, CLEAR_STATE_PROGRAM


# def createApp(client: AlgodClient, sender: account):
#     approval_program, clear_state_program = get_smart_contract(client)
#     global_schema = transaction.StateSchema(num_uints=0, num_byte_slices=0)
#     local_schema = transaction.StateSchema(num_uints=0, num_byte_slices=0)
#     app_args = []
    
#     txn = transaction.ApplicationCreateTxn(
#         sender=sender
#     )


# def createToken():


@csrf_exempt
def process_products(request):
    input_body = loads(request.body)
    print(input_body['customer_wallet'])
    reward = 0
    for item in input_body['products']:
        reward += Products.objects.get(id=item['id']).rating * item['price'] * item['amount'] * 1000
    print(reward)
    # appCallTxn = transaction.ApplicationCallTxn(
    #     sender=
    # )
    return HttpResponse(status=200)
    

@csrf_exempt
def add_product(request):
    input_body = loads(request.body)

    return HttpResponse(status=200)
    
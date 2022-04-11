from click import confirm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from json import loads
from pyteal import OnComplete

from pytest import param
from .models import *
from base64 import b64decode
from typing import Tuple
from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from algosdk.future.transaction import AssetTransferTxn, ApplicationCallTxn, wait_for_confirmation
from algosdk import account, mnemonic
# from pyteal import compileTeal, Mode, Expr
# from .smart_contract import approval_program, clear_state_program

# Create your views here.

ALGOD_ADDRESS = "http://localhost:4001"
ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ASSET_ID = 20
APP_ID = 17

def get_algod_client() -> AlgodClient:
    return AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)


@csrf_exempt
def get_tokens(request):
    algod_client = get_algod_client()
    mnemonic01 = "biology pulp scrub rebuild velvet question ring weasel legend gap merit gallery twenty toss unfair novel ancient output mesh present excess decide champion absent fish"
    private_key = mnemonic.to_private_key(mnemonic01)
    public_key = account.address_from_private_key(private_key)
    # acc01 = account.generate_account()
    # print("Public key: " + acc01['pk'])
    # print(mnemonic.from_private_key(acc01[0]))
    # print(acc01[0])
    # print(acc01[1])
    # print(algod_client.suggested_params())
    params = algod_client.suggested_params()
    account_info = algod_client.account_info(public_key)
    holding = None
    i = 0
    for my_acc_info in account_info['assets']:
        asset = account_info['assets'][i]
        i = i + 1
        if (asset['asset-id'] == ASSET_ID):
            holding = True
            break

    # for asset in account_info['assets']:
    #     if (asset['asset-id'] == ASSET_ID):
    #         holding = True
    #         break

    if not holding:
        txn = AssetTransferTxn(
            sender=public_key,
            sp=params,
            receiver=public_key,
            amt=0,
            index=ASSET_ID
        )
        stxn = txn.sign(private_key)
        try:
            txid = algod_client.send_transaction(stxn)
            confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
            print("txID: ", txid)
            print("round: ", confirmed_txn['confirmed-round'])
        except Exception as err:
            print(err)

    app_args = [
        b"send_asa",
        1000
    ]

    txn = ApplicationCallTxn(
        sender=public_key, 
        sp=params, 
        on_complete=transaction.OnComplete.NoOpOC,
        index=APP_ID, 
        app_args=app_args,
        foreign_assets=[20]
    )

    stxn = txn.sign(private_key)
    try:
        txid = algod_client.send_transaction(stxn)
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("txID:", txid)
        print("round:", confirmed_txn['confirmed-round'])
    except Exception as err:
        print(err)

    return HttpResponse(status=200)


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
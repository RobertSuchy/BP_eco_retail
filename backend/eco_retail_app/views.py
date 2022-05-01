from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import *
from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from algosdk.future.transaction import AssetTransferTxn, ApplicationCallTxn, wait_for_confirmation
from algosdk import account, mnemonic
from algosdk import encoding


class AuthRegister(View):
    def get(self, requwst):
        return HttpResponse()


ALGOD_ADDRESS = "http://localhost:4001"
ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ASSET_ID = 20
APP_ID = 17


def get_algod_client() -> AlgodClient:
    return AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)


@csrf_exempt
def get_tokens(request):
    print(".............................................")
    print(request.body)
    print(".............................................")
    public_key = request.body.decode()
    print(".............................................")
    print(public_key)
    print(".............................................")
    algod_client = get_algod_client()
    # mnemonic01 = "biology pulp scrub rebuild velvet question ring weasel legend gap merit gallery twenty toss unfair novel ancient output mesh present excess decide champion absent fish"
    # private_key = mnemonic.to_private_key(mnemonic01)
    # public_key = account.address_from_private_key(private_key)
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

    if not holding:
        txn = AssetTransferTxn(
            sender=public_key,
            sp=params,
            receiver=public_key,
            amt=0,
            index=ASSET_ID
        )
        # stxn = txn.sign(private_key)
        # try:
        #     txid = algod_client.send_transaction(stxn)
        #     confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        #     print("txID: ", txid)
        #     print("round: ", confirmed_txn['confirmed-round'])
        # except Exception as err:
        #     print(err)

    # app_args = [
    #     b"send_asa",
    #     1000
    # ]

    # txn = ApplicationCallTxn(
    #     sender=public_key, 
    #     sp=params, 
    #     on_complete=transaction.OnComplete.NoOpOC,
    #     index=APP_ID, 
    #     app_args=app_args,
    #     foreign_assets=[20]
    # )

    # stxn = txn.sign(private_key)
    # try:
    #     txid = algod_client.send_transaction(stxn)
    #     confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    #     print("txID:", txid)
    #     print("round:", confirmed_txn['confirmed-round'])
    # except Exception as err:
    #     print(err)

    print(".............................................")
    print(txn)
    print(".............................................")

    print(".............................................")
    print(encoding.msgpack_encode(txn))
    print(".............................................")

    return HttpResponse(encoding.msgpack_encode(txn), status=200)


@csrf_exempt
def process_products(request):
    input_body = json.loads(request.body)
    print(input_body['customer_wallet'])
    reward = 0
    for item in input_body['products']:
        reward += Product.objects.get(id=item['id']).rating * item['price'] * item['amount'] * 1000
    print(reward)
    # appCallTxn = transaction.ApplicationCallTxn(
    #     sender=
    # )
    return HttpResponse(status=200)
    

@csrf_exempt
def add_product(request):
    input_body = json.loads(request.body)
    now = timezone.now()
    Product.objects.create(
        name=input_body['name'],
        rating=input_body['rating'],
        created_at=now,
        updated_at=now
    )    
    return HttpResponse(status=200)
    
import email
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.views import View
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import UserSerializer
from .models import *
import json

from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from algosdk.future.transaction import AssetTransferTxn, ApplicationCallTxn, wait_for_confirmation
from algosdk import account, mnemonic
from algosdk import encoding


ALGOD_ADDRESS = "http://localhost:4001"
ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ASSET_ID = 4
APP_ID = 10
ALGOD_CLIENT = AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)


@method_decorator(csrf_exempt, name='dispatch')
class OptInAssetGetTxn(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        body = json.loads(request.body)
        public_key = body['wallet']
        params = ALGOD_CLIENT.suggested_params()
        account_info = ALGOD_CLIENT.account_info(public_key)
        holding = False
        for asset in account_info['assets']:
            if asset['asset-id'] == ASSET_ID:
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
            return Response(encoding.msgpack_encode(txn))

        return Response(None)


@method_decorator(csrf_exempt, name='dispatch')
class OptInContractGetTxn(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        body = json.loads(request.body)
        public_key = body['wallet']
        params = ALGOD_CLIENT.suggested_params()
        account_info = ALGOD_CLIENT.account_info(public_key)
        opted_in = False
        for app in account_info['apps-local-state']:
            if app['id'] == APP_ID:
                opted_in = True
                break

        if not opted_in:
            txn = transaction.ApplicationOptInTxn(
                sender=public_key,
                sp=params,
                index=APP_ID,
                app_args=body['user_type']
            )
            return Response(encoding.msgpack_encode(txn))

        return Response(None)


@method_decorator(csrf_exempt, name='dispatch')
class OptInSendTxn(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        signed_txn = encoding.future_msgpack_decode(request.body)
        try:
            txid = ALGOD_CLIENT.send_transaction(signed_txn)
            confirmed_txn = wait_for_confirmation(ALGOD_CLIENT, txid, 4)
            print("txID: ", txid)
            print("round: ", confirmed_txn['confirmed-round'])
        except Exception as err:
            print(err)
            return Response('err')

        return Response('opted-in')


@method_decorator(csrf_exempt, name='dispatch')
class AuthRegister(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        request_body = json.loads(request.body)
        now = timezone.now()
        user_model = get_user_model()
        try:
            user = user_model.objects.create_user(
                email=request_body['email'],
                user_type=request_body['userType'],
                wallet=request_body['wallet'],
                password=request_body['password'],
                created_at=now,
                updated_at=now
            )    
            serializer = UserSerializer(user)
            return Response(serializer.data)
        
        except Exception as err:
            print(err)
            return Response(status=500)



@method_decorator(csrf_exempt, name='dispatch')
class AuthLogout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        content = {'message': 'Logout successfully'}
        return Response(content)


@method_decorator(csrf_exempt, name='dispatch')
class AuthMe(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


@csrf_exempt
def get_tokens(request):
    algod_client = get_algod_client()
    # private_key = mnemonic.to_private_key(mnemonic01)
    # public_key = account.address_from_private_key(private_key)
    params = algod_client.suggested_params()

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

    return HttpResponse(encoding.msgpack_encode(txn))


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
    return HttpResponse()
    

@csrf_exempt
def add_product(request):
    request_body = json.loads(request.body)
    now = timezone.now()
    Product.objects.create(
        name=request_body['name'],
        rating=request_body['rating'],
        created_at=now,
        updated_at=now
    )    
    return HttpResponse()

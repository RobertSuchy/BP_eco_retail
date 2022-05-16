from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer
from .models import *
import json

from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from algosdk import encoding


ALGOD_ADDRESS = "http://localhost:4001"
ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ASSET_ID = 22
APP_ID = 19
APP_ACCOUNT = "Y5NP7DMHLJWMKUNZGKGG62TLLZEYE4AUYI7UV3NE7N2DNVK7WHD6RZW5WQ"
ALGOD_CLIENT = AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)
PARAMS = ALGOD_CLIENT.suggested_params()


@method_decorator(csrf_exempt, name='dispatch')
class OptInAssetGetTxn(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        body = json.loads(request.body)
        public_key = body['wallet']
        account_info = ALGOD_CLIENT.account_info(public_key)
        holding = False
        for asset in account_info['assets']:
            if asset['asset-id'] == ASSET_ID:
                holding = True
                break

        if not holding:
            txn = transaction.AssetTransferTxn(
                sender=public_key,
                sp=PARAMS,
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
        account_info = ALGOD_CLIENT.account_info(public_key)
        opted_in = False
        for app in account_info['apps-local-state']:
            if app['id'] == APP_ID:
                opted_in = True
                break

        if not opted_in:
            txn = transaction.ApplicationOptInTxn(
                sender=public_key,
                sp=PARAMS,
                index=APP_ID,
                app_args=[body['user_type']]
            )
            return Response(encoding.msgpack_encode(txn))

        return Response(None)


# used for sending opt-in transactions during registration, without authentication
@method_decorator(csrf_exempt, name='dispatch')
class OptInSendTxn(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        body = json.loads(request.body)
        signed_txn = encoding.future_msgpack_decode(body['signed_txn'])
        try:
            txid = ALGOD_CLIENT.send_transaction(signed_txn)
            confirmed_txn = transaction.wait_for_confirmation(ALGOD_CLIENT, txid, 4)
            print("txID: ", txid)
            print("round: ", confirmed_txn['confirmed-round'])
        except Exception as err:
            print(err)
            return Response(status=500)

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
class AuthGetToken(ObtainAuthToken):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data['credentials'])
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if UserSerializer(user).data['wallet'] == request.data['wallet']:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})

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


@method_decorator(csrf_exempt, name='dispatch')
class GetAccountBalance(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        body = json.loads(request.body)
        public_key = body['wallet']
        account_info = ALGOD_CLIENT.account_info(public_key)
        algos = account_info['amount'] / 1_000_000
        ecoCoins = 0
        for asset in account_info['assets']:
            if asset['asset-id'] == ASSET_ID:
                ecoCoins = asset['amount']
                break

        response = {
            'algos': algos,
            'ecoCoins': ecoCoins
        }

        return Response(response)


@method_decorator(csrf_exempt, name='dispatch')
class BuyEcoCoinsGetTxn(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        body = json.loads(request.body)
        public_key = body['wallet']
        amount = body['amount']
        print(amount)
        app_args = [
            b"exchange_asa",
            amount
        ]

        txn1 = transaction.ApplicationCallTxn(
            sender=public_key,
            sp=PARAMS,
            on_complete=transaction.OnComplete.NoOpOC,
            index=APP_ID,
            app_args=app_args,
            foreign_assets=[ASSET_ID]
        )

        txn2 = transaction.PaymentTxn(
            sender=public_key,
            sp=PARAMS,
            receiver=APP_ACCOUNT,
            # EcoRetail Coins -> Algos -> microAlgos
            amt=int(int(amount) / 100 * 1_000_000)
        )

        group_id = transaction.calculate_group_id([txn1, txn2])
        txn1.group = group_id
        txn2.group = group_id
        txn_group = [
            encoding.msgpack_encode(txn1),
            encoding.msgpack_encode(txn2)
        ]

        return Response(txn_group)


# used for sending transactions or transaction groups with authentication
@method_decorator(csrf_exempt, name='dispatch')
class SendTxn(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        body = json.loads(request.body)
        signed_txn_str = body['signed_txn']
        is_list = isinstance(signed_txn_str, list)
        if is_list:
            signed_txn_group = []
            for txn in signed_txn_str:
                signed_txn_group.append(encoding.future_msgpack_decode(txn))
        else:
            signed_txn = encoding.future_msgpack_decode(signed_txn_str)

        try:
            if is_list:
                txid = ALGOD_CLIENT.send_transactions(signed_txn_group)
            else:
                txid = ALGOD_CLIENT.send_transaction(signed_txn)
            confirmed_txn = transaction.wait_for_confirmation(ALGOD_CLIENT, txid, 4)
            print("txID: ", txid)
            print("round: ", confirmed_txn['confirmed-round'])
        except Exception as err:
            print(err)
            return Response(status=500)

        return Response('transaction(s) sent successfully')


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
    return Response()
    

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
    return Response()

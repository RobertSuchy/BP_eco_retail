from unicodedata import category
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

from .serializers import ProductSerializer, RewardsPolicySerializer, UserSerializer
from .models import *
import json

from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from algosdk import encoding


ALGOD_ADDRESS = "http://localhost:4001"
ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ASSET_ID = 22
APP_ID = 19
APP_ACCOUNT = "IENLVNK7TDN6X3W26JGMRDT2RKKNX7CYVRGJTTUV34O54NXHNQ3C7DA5TA"
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
                index=ASSET_ID,
                note=str(timezone.now())
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
                app_args=[body['user_type']],
                note=str(timezone.now())
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
                name=request_body['name'],
                wallet=request_body['wallet'],
                password=request_body['password'],
                created_at=now,
                updated_at=now
            )    

            if request_body['userType'] == 'chainStore':
                RewardsPolicy.objects.create(
                    chain_store=user,
                    category_a=2,
                    category_b=1.5,
                    category_c=1,
                    category_d=0.5,
                    category_e=0.25,
                    category_f=0,
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
        user_serializer = UserSerializer(user)
        if user_serializer.data['user_type'] == 'chainStore':
            rewards_policy = RewardsPolicy.objects.get(chain_store=user)
            rewards_policy_serializer = RewardsPolicySerializer(rewards_policy)
            return Response([user_serializer.data, rewards_policy_serializer.data])

        return Response(user_serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateRewardsPolicy(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_body = json.loads(request.body)
        try:
            rewardsPolicy = RewardsPolicy.objects.get(chain_store=request.user)
            now = timezone.now()
            rewardsPolicy.category_a = request_body['categoryA']
            rewardsPolicy.category_b = request_body['categoryB']
            rewardsPolicy.category_c = request_body['categoryC']
            rewardsPolicy.category_d = request_body['categoryD']
            rewardsPolicy.category_e = request_body['categoryE']
            rewardsPolicy.category_f = request_body['categoryF']
            rewardsPolicy.updated_at = now
            rewardsPolicy.save()

            return Response()

        except Exception as err:
            print(err)
            return Response(status=500)


@method_decorator(csrf_exempt, name='dispatch')
class GetAccountBalance(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        public_key = serializer.data['wallet']        
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
        serializer = UserSerializer(request.user)
        public_key = serializer.data['wallet']
        amount = body['amount']
        app_args = [
            b"exchange_asa",
            int(amount)
        ]

        txn1 = transaction.ApplicationCallTxn(
            sender=public_key,
            sp=PARAMS,
            on_complete=transaction.OnComplete.NoOpOC,
            index=APP_ID,
            app_args=app_args,
            foreign_assets=[ASSET_ID],
            note=str(timezone.now())
        )

        txn2 = transaction.PaymentTxn(
            sender=public_key,
            sp=PARAMS,
            receiver=APP_ACCOUNT,
            # EcoRetail Coins -> Algos -> microAlgos
            amt=int(int(amount) / 100 * 1_000_000),
            note=str(timezone.now())
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

        return Response('Transaction(s) sent successfully!')


@method_decorator(csrf_exempt, name='dispatch')
class AddProduct(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        public_key = serializer.data['wallet']

        app_args = [
            b"add_product"
        ]

        txn = transaction.ApplicationCallTxn(
            sender=public_key,
            sp=PARAMS,
            on_complete=transaction.OnComplete.NoOpOC,
            index=APP_ID,
            app_args=app_args,
            note=str(timezone.now())
        )

        return Response(encoding.msgpack_encode(txn))

    def post(self, request):
        request_body = json.loads(request.body)
        now = timezone.now()
        try:
            product, created = Product.objects.update_or_create(
                name=request_body['name'],
                producer=request.user,
                defaults={
                'name': request_body['name'],
                'producer': request.user,
                'description': request_body['description'],
                'rating': request_body['rating'],
                'created_at': now,
                'updated_at': now
                }
            )
            return Response(created)
        
        except Exception as err:
            print(err)
            return Response(status=500)        


@method_decorator(csrf_exempt, name='dispatch')
class GetAllProducts(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        serializedProducts = []
        for product in products:
            serializedProducts.append(ProductSerializer(product).data)

        return Response(serializedProducts)


@method_decorator(csrf_exempt, name='dispatch')
class ProcessProducts(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(request):
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
    
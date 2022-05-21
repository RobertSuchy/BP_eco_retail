# from datetime import datetime
# import random
import json
from locust import HttpUser, constant_throughput, task
from algosdk import mnemonic, encoding


class Test(HttpUser):
    private_key = None
    def on_start(self):
        mnemonic01 = "transfer innocent power seat business wrestle valve tomato thank bulb pond gun gaze retreat museum solution veteran swift enter crop police boy renew abstract spawn"
        self.private_key = mnemonic.to_private_key(mnemonic01)
        self.client.headers.update({'Authorization': 'Token a4b5b36fe6e1ff29749e4dddcd87fc2ba7839bc1'})
        
    @task
    def process_purchase(self):
        # time = datetime.now()
        # r = random.randint(0, 1)
        # if r == 1:
        data = {
            "wallet":"UOGHQT4VW23V56C4YEIGY7PVCRADTZSOZI3SCIIGDOIXJ4SI2P4LNAF3VI",
            "purchase_list":[
                {"id":1,"amount":2,"price":0.01},
                {"id":2,"amount":3,"price":0.04},
                {"id":3,"amount":1,"price":0.05},
                {"id":4,"amount":4,"price":0.03},
                {"id":5,"amount":6,"price":0.01},
                {"id":6,"amount":5,"price":0.02},
                {"id":7,"amount":1,"price":0.05},
                {"id":8,"amount":4,"price":0.03},
                {"id":9,"amount":2,"price":0.04}
            ],
            "algo_price":"0.42"
        }
        # else:
        #     data = {
        #         "wallet":"TX4MJ32LKKDKW3YD2MDB2BX5AQBV7J4QPO6YYLUCCMDXMXL26GPUNHGKFM",
        #         # "purchase_list":[{"id":1,"amount":5,"price":0.15},{"id":2,"amount":15,"price":0.075},{"id":3,"amount":2,"price":0.14}],
        #         "purchase_list":[{"id":1,"amount":5,"price":0.15}],
        #         "algo_price":"0.42"
        #     }            
            
        txn = json.loads(self.client.post("api/process-purchase/", json.dumps(data)).content)[1]

        signed_txn = [
            encoding.future_msgpack_decode(txn[0]).sign(self.private_key),
            encoding.future_msgpack_decode(txn[1]).sign(self.private_key),
        ]

        signed_txn = [
            encoding.msgpack_encode(signed_txn[0]),
            encoding.msgpack_encode(signed_txn[1])
        ]

        self.client.post("api/send-txn/", json.dumps({ "signed_txn": signed_txn }))
        # self.client.cookies.clear()

    # wait_time = constant_throughput(0.1)

# from datetime import datetime
# import random
import json
from locust import HttpUser, constant_throughput, task
from algosdk import mnemonic, encoding


class Test(HttpUser):
    private_key = None
    def on_start(self):
        mnemonic01 = "example canyon property gentle mention solve spring shoot twelve truly winner card absent process dawn tube shoot clip hundred advance fantasy loyal gap abandon right"
        self.private_key = mnemonic.to_private_key(mnemonic01)
        self.client.headers.update({'Authorization': 'Token 67f61770b81306bdb2ef2e3a2e2d18f2c05a53aa'})
        
    @task
    def process_purchase(self):
        # time = datetime.now()
        # r = random.randint(0, 1)
        # if r == 1:
        data = {
            "wallet":"PGP2FSYJG4HPVMXIWTEBZCH2JXWU5AHYUZZ6BE6V4ZYRI2SUNMIYAJ2Y2Y",
            "purchase_list":[
                {"id":1,"amount":1,"price":0.005},
                # {"id":2,"amount":3,"price":0.004},
                # {"id":3,"amount":1,"price":0.005},
                # {"id":4,"amount":4,"price":0.003},
                # {"id":5,"amount":6,"price":0.001},
                # {"id":6,"amount":5,"price":0.002},
                # {"id":7,"amount":1,"price":0.005},
                # {"id":8,"amount":4,"price":0.003},
                # {"id":9,"amount":2,"price":0.004}
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

import { api } from 'src/boot/axios'

class TxnService {
  async optInAssetGetTxn (wallet: string) {
    const response = await api.post('opt-in-asset-get-txn/', { wallet })
    return response.data
  }

  async optInContractGetTxn (wallet: string, userType: string) {
    const response = await api.post('opt-in-contract-get-txn/', { wallet, user_type: userType })
    return response.data
  }

  async optInSendTxn (signedTxn: string) {
    const response = await api.post('opt-in-send-txn/', { signed_txn: signedTxn })
    return response.data
  }

  async getAccountBalance (wallet: string) {
    const response = await api.post('get-account-balance/', { wallet })
    return response.data
  }

  async buyEcoCoinsGetTxn (wallet: string, amount: number) {
    const response = await api.post('buy-eco-coins-get-txn/', { wallet, amount })
    return response.data
  }
}

export default new TxnService()

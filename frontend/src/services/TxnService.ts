import { api } from 'src/boot/axios'

class TxnService {
  async optInAssetGetTxn (wallet: string) {
    const response = await api.post('opt-in-asset-get-txn/', wallet)
    return response.data
  }

  async optInContractGetTxn (wallet: string) {
    const response = await api.post('opt-in-contract-get-txn/', wallet)
    return response.data
  }

  async optInSendTxn (signedTxn: string) {
    const response = await api.post('opt-in-send-txn/', signedTxn)
    return response.data
  }
}

export default new TxnService()

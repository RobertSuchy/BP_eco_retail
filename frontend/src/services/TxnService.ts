import { api } from 'src/boot/axios'

class TxnService {
  async optInGetTxn (wallet: string) {
    const response = await api.post('opt-in-get-txn/', wallet)
    return response.data
  }

  async optInSendTxn (signedTxn: string) {
    const response = await api.post('opt-in-send-txn/', signedTxn)
    return response.data
  }
}

export default new TxnService()

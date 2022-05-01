import type { AxiosError, AxiosRequestConfig } from 'axios'
import type { ApiToken, LoginCredentials, RegisterData, User } from 'src/contracts'
import { api } from 'src/boot/axios'

class TxnService {
  async optIn (wallet: string) {
    const response = await api.post('get-tokens/', wallet)
    console.log(response.data)
    // return response.data
  }
}

export default new TxnService()

import type { AxiosError, AxiosRequestConfig } from 'axios'
import type { ApiToken, LoginCredentials, RegisterData, User } from 'src/contracts'
import { api } from 'src/boot/axios'

class AuthService {
  async me (wallet: string, dontTriggerLogout = false): Promise<User | null> {
    return api.post(
      'auth/me/', { wallet }, { dontTriggerLogout } as AxiosRequestConfig
    )
      .then((response) => response.data)
      .catch((error: AxiosError) => {
        if (error.response?.status === 401) {
          return null
        }

        return Promise.reject(error)
      })
  }

  async register (data: RegisterData): Promise<User> {
    const response = await api.post<User>('auth/register/', data)
    return response.data
  }

  async login (credentials: LoginCredentials, wallet: string): Promise<ApiToken> {
    const response = await api.post<ApiToken>('auth/login/', { credentials, wallet })
    return response.data
  }

  async logout (): Promise<void> {
    await api.post('auth/logout/')
  }
}

export default new AuthService()

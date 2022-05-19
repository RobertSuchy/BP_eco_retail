import { ActionTree } from 'vuex'
import { StateInterface } from '../index'
import { AuthStateInterface } from './state'
import { authService, authManager, txnService } from 'src/services'
import { LoginCredentials, RegisterData } from 'src/contracts'

const actions: ActionTree<AuthStateInterface, StateInterface> = {
  async check ({ commit, dispatch }) {
    try {
      commit('AUTH_START')
      const response = await authService.me()
      if (response) {
        await dispatch('products/getAllProducts', '', { root: true })
        await dispatch('products/getCustomers', '', { root: true })

        const balance = await txnService.getAccountBalance()

        if (Array.isArray(response)) {
          const user = response[0]
          const rewardsPolicy = response[1]
          user.algos = balance.algos
          user.ecoCoins = balance.ecoCoins
          commit('AUTH_SUCCESS', { user, rewardsPolicy })
        } else {
          const user = response
          user.algos = balance.algos
          user.ecoCoins = balance.ecoCoins
          commit('AUTH_SUCCESS', { user, rewardsPolicy: null })
        }
      }
      return response !== null
    } catch (err) {
      commit('AUTH_ERROR', err)
      throw err
    }
  },
  async register ({ commit }, form: RegisterData) {
    try {
      commit('AUTH_START')
      const user = await authService.register(form)
      commit('AUTH_SUCCESS', { user: null, rewardsPolicy: null })
      return user
    } catch (err) {
      commit('AUTH_ERROR', err)
      throw err
    }
  },
  async login ({ commit }, { credentials, wallet }: { credentials: LoginCredentials, wallet: string }) {
    try {
      commit('AUTH_START')
      const apiToken = await authService.login(credentials, wallet)
      commit('AUTH_SUCCESS', { user: null, rewardsPolicy: null })
      // save api token to local storage and notify listeners
      authManager.setToken(apiToken.token)
      return apiToken
    } catch (err) {
      commit('AUTH_ERROR', err)
      throw err
    }
  },
  async logout ({ commit }) {
    try {
      commit('AUTH_START')
      await authService.logout()
      commit('AUTH_SUCCESS', { user: null, rewardsPolicy: null })
      // remove api token and notify listeners
      authManager.removeToken()
    } catch (err) {
      commit('AUTH_ERROR', err)
      throw err
    }
  }
}

export default actions

import { ActionTree } from 'vuex'
import { StateInterface } from '../index'
import { AuthStateInterface } from './state'
import { authService, authManager, txnService } from 'src/services'
import { LoginCredentials, RegisterData } from 'src/contracts'
import MyAlgoConnect from '@randlabs/myalgo-connect'

const actions: ActionTree<AuthStateInterface, StateInterface> = {
  async check ({ commit }, wallet: string) {
    try {
      commit('AUTH_START')
      const user = await authService.me(wallet)
      if (user) {
        const balance = await txnService.getAccountBalance(user.wallet)
        user.algos = balance.algos
        user.ecoCoins = balance.ecoCoins
      }
      commit('AUTH_SUCCESS', user)
      return user !== null
    } catch (err) {
      commit('AUTH_ERROR', err)
      throw err
    }
  },
  async register ({ commit }, form: RegisterData) {
    try {
      commit('AUTH_START')
      const user = await authService.register(form)
      commit('AUTH_SUCCESS', null)
      return user
    } catch (err) {
      commit('AUTH_ERROR', err)
      throw err
    }
  },
  async login ({ commit }, { credentials, wallet, myAlgoConnect }: { credentials: LoginCredentials, wallet: string, myAlgoConnect: MyAlgoConnect }) {
    try {
      commit('AUTH_START')
      const apiToken = await authService.login(credentials, wallet)
      commit('AUTH_STORE_MY_ALGO_CONNECT', myAlgoConnect)
      commit('AUTH_SUCCESS', null)
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
      commit('AUTH_SUCCESS', null)
      // remove api token and notify listeners
      authManager.removeToken()
    } catch (err) {
      commit('AUTH_ERROR', err)
      throw err
    }
  }
}

export default actions

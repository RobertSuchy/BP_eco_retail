import { GetterTree } from 'vuex'
import { StateInterface } from '../index'
import { AuthStateInterface } from './state'

const getters: GetterTree<AuthStateInterface, StateInterface> = {
  isAuthenticated (context) {
    return context.user !== null
  },

  getUser (context) {
    return context.user
  },

  getUserType (context) {
    return context.user?.userType
  },

  getMyAlgoConnect (context) {
    return context.myAlgoConnect
  }
}

export default getters

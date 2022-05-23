// autentifikačný aparát pre frontend sme použili so súhlasom Ing. Eduard Kuric, PhD.
// poskytnutého k predmetu Vývoj progresívnych webových aplikácii
// https://github.com/kurice/vpwa22/tree/main/prednasky/slek/part2

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
  }
}

export default getters

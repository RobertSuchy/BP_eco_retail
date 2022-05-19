import { productService } from 'src/services'
import { ActionTree } from 'vuex'
import { StateInterface } from '../index'
import { ProductsStateInterface } from './state'

const actions: ActionTree<ProductsStateInterface, StateInterface> = {
  async getAllProducts ({ commit }) {
    const products = await productService.getAllProducts()
    commit('STORE_PRODUCTS', products)
  },

  async getCustomers ({ commit }) {
    const customers = await productService.getCustomers()
    commit('STORE_CUSTOMERS', customers)
  }
}

export default actions

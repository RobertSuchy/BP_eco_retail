import { GetterTree } from 'vuex'
import { StateInterface } from '../index'
import { ProductsStateInterface } from './state'

const getters: GetterTree<ProductsStateInterface, StateInterface> = {
  getAllProducts (context) {
    return context.products
  },

  getCustomers (context) {
    return context.customers
  },

  getProducersProducts: (context) => (producerName: string) => {
    return context.products.filter(product => product.producerName === producerName)
  }
}

export default getters

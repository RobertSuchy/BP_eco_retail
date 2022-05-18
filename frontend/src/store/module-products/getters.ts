import { GetterTree } from 'vuex'
import { StateInterface } from '../index'
import { ProductsStateInterface } from './state'

const getters: GetterTree<ProductsStateInterface, StateInterface> = {
  getAllProducts (context) {
    return context.products
  },

  getProducersProducts: (context) => (producerName: string) => {
    return context.products.filter(product => product.producerName === producerName)
  }
}

export default getters

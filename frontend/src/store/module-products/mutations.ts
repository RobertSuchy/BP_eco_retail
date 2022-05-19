import { Product } from 'src/contracts'
import { MutationTree } from 'vuex'
import { ProductsStateInterface } from './state'

const mutation: MutationTree<ProductsStateInterface> = {
  STORE_PRODUCTS (state, products: Product[]) {
    state.products = products
  },

  STORE_CUSTOMERS (state, customers: string[]) {
    state.customers = customers
  }
}

export default mutation

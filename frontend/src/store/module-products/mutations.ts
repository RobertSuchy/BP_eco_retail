import { Product } from 'src/contracts'
import { MutationTree } from 'vuex'
import { ProductsStateInterface } from './state'

const mutation: MutationTree<ProductsStateInterface> = {
  STORE_PRODUCTS (state, products: Product[]) {
    state.products = products
  }
}

export default mutation

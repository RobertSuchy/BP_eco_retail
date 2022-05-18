import { Product } from 'src/contracts'

export interface ProductsStateInterface {
  products: Product[]
}

function state(): ProductsStateInterface {
  return {
    products: []
  }
}

export default state

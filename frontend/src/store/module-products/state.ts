import { Product } from 'src/contracts'

export interface ProductsStateInterface {
  products: Product[],
  customers: string[]
}

function state(): ProductsStateInterface {
  return {
    products: [],
    customers: []
  }
}

export default state

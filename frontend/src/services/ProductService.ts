import { api } from 'src/boot/axios'
import { ProductForm, RewardsPolicy } from 'src/contracts'

class ProductService {
  async addProduct (productForm: ProductForm) {
    const response = await api.post('add-product/', productForm)
    return response.data
  }

  async getAllProducts () {
    const response = await api.get('get-all-products/')
    return response.data
  }

  async updateRewardsPolicy (rewardsPolicy: RewardsPolicy) {
    const response = await api.post('update-rewards-policy/', rewardsPolicy)
    return response.data
  }

  async getCustomers () {
    const response = await api.get('get-customers')
    return response.data
  }

  async processPurchase (wallet: string, purchaseList: { id: number, amount: number, price: number }[], algoPrice: number) {
    const response = await api.post('process-purchase/', { wallet, purchase_list: purchaseList, algo_price: algoPrice })
    return response.data
  }
}

export default new ProductService()

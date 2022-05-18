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
}

export default new ProductService()

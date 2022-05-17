import { api } from 'src/boot/axios'
import { ProductForm } from 'src/contracts/Product'

class ProductService {
  async addProduct (productForm: ProductForm) {
    const response = await api.post('add-product/', productForm)
    return response.data
  }
}

export default new ProductService()

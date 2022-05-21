<template>
  <q-page class="column items-center justify-evenly">
    <q-table
    title="All products in database"
    :rows="getAllProducts"
    :columns="columns"
    row-key="id"
    :dense="$q.screen.lt.md"
    wrap-cells
    virtual-scroll
    :rows-per-page-options="[0]"
    class="q-ma-md q-ma-md-lg q-pa-xs q-pa-md-md q-pa-lg-lg"
    style="height: 50vh"
    :style="$q.screen.lt.sm ? {'width': '90%'} : $q.screen.lt.md ? {'width': '80%'} : $q.screen.lt.lg ? {'width': '70%'} : {'width': '60%'}"
    />

    <q-card v-if="getUser.userType === 'chainStore'" class="column q-ma-md q-ma-md-lg q-pa-xs q-pa-md-md q-pa-lg-lg flex justify-center"
      :style="$q.screen.lt.sm ? {'width': '90%'} : $q.screen.lt.md ? {'width': '50%'} : $q.screen.lt.lg ? {'width': '45%'} : {'width': '35%'}">
        <q-card-section class="flex justify-center q-pb-xs">
          <div class="text-h5">
            Create a purchase list
          </div>
        </q-card-section>

        <q-separator class="q-my-sm" />

        <div class="row flex justify-evenly">
          <q-form class="col-12 col-lg-6 q-gutter-xs" @submit="submitProduct" >
            <q-card-section class="q-gutter-y-sm">
              <q-input
                      name="id"
                      type="number"
                      v-model.number="productForm.id"
                      label="Product ID"
                      :rules="[val => !!val || 'Product id is required!']"
                      lazy-rules="ondemand"
                      dense
                      filled
                      clearable
                      autofocus>
                <template v-slot:prepend>
                  <q-icon name="label" />
                </template>
              </q-input>

              <q-input
                      name="amount"
                      type="number"
                      v-model.number="productForm.amount"
                      label="Amount"
                      :rules="[
                        val => !!val || 'Amount is required'
                      ]"
                      lazy-rules="ondemand"
                      dense
                      filled
                      clearable>
                <template v-slot:prepend>
                  <q-icon name="description" />
                </template>
              </q-input>

              <q-input
                      name="price"
                      type="number"
                      mask="#.##"
                      fill-mask="0"
                      reverse-fill-mask
                      step="0.01"
                      v-model.number="productForm.price"
                      label="Price"
                      :rules="[val => !!val || 'Price is required!']"
                      lazy-rules="ondemand"
                      dense
                      filled
                      clearable>
                <template v-slot:prepend>
                  <q-icon name="euro" />
                </template>
              </q-input>

            </q-card-section>

            <q-card-actions class="flex justify-center">
              <q-btn outline rounded color="secondary" size="md" class="full-width" label="Add product to purchase list" type="submit" />
            </q-card-actions>
          </q-form>

          <div class="col-12 col-lg-6 flex justify-center">
            {{ purchaseList }}
          </div>
        </div>

        <q-card-section class="flex justify-center q-pb-xs">
          <div class="text-h5">
            Confirm purchase list
          </div>
        </q-card-section>

        <q-separator class="q-my-sm" />

        <q-form class="col-6 q-gutter-xs" @submit="submitPurchase" >
          <q-card-section class="q-gutter-y-sm">
            <q-select
                    class="text-caption"
                    name="wallet"
                    type="text"
                    v-model="wallet"
                    :options="getCustomers"
                    label="Customer's wallet address"
                    :rules="[val => !!val || 'Wallet address is required!']"
                    lazy-rules="ondemand"
                    dense
                    filled
                    clearable>
              <template v-slot:prepend>
                <q-icon name="wallet" />
              </template>
            </q-select>
          </q-card-section>

          <q-card-actions class="flex justify-center">
            <q-btn outline rounded color="secondary" size="md" class="full-width" label="Confirm and send reward to customer" type="submit" />
          </q-card-actions>
        </q-form>
      </q-card>
  </q-page>
</template>

<script lang="ts">
import MyAlgoConnect, { AlgorandTxn } from '@randlabs/myalgo-connect'
import { QTableProps } from 'quasar'
import { defineComponent } from 'vue'
import { mapGetters } from 'vuex'
import { productService, txnService } from '../services'

export default defineComponent({
  name: 'ProductsPage',
  data() {
    return {
      columns: [
        {
          name: 'id',
          required: true,
          label: 'Product ID',
          field: 'id',
          sortable: true,
          align: 'center'
        },
        {
          name: 'name',
          required: true,
          label: 'Name',
          field: 'name',
          sortable: true,
          align: 'left'
        },
        {
          name: 'producerName',
          required: true,
          label: 'Producer name',
          field: 'producerName',
          sortable: true,
          align: 'left'
        },
        {
          name: 'description',
          required: false,
          label: 'Description',
          field: 'description',
          sortable: false,
          align: 'left'
        },
        {
          name: 'rating',
          required: true,
          label: 'Eco rating',
          field: 'rating',
          sortable: true,
          align: 'center'
        }
      ] as QTableProps['columns'],
      productForm: {
        id: 0,
        amount: 0,
        price: 0.00
      },
      purchaseList: [] as { id: number, amount: number, price: number }[],
      wallet: ''
    }
  },

  computed: {
    ...mapGetters('auth', {
      getUser: 'getUser'
    }),
    ...mapGetters('products', {
      getAllProducts: 'getAllProducts',
      getCustomers: 'getCustomers'
    })
  },

  methods: {
    async submitProduct() {
      if (this.productForm.amount < 1) {
        this.$q.notify({
          type: 'negative',
          position: 'bottom',
          message: 'Amount must be greater than 0!'
        })
        return
      }
      this.purchaseList.push({
        id: this.productForm.id,
        amount: this.productForm.amount,
        price: this.productForm.price
      })
      this.productForm.id = 0
      this.productForm.amount = 0
      this.productForm.price = 0
    },

    async submitPurchase() {
      const algoPrice = await txnService.getAlgoPrice()
      productService.processPurchase(this.wallet, this.purchaseList, algoPrice).then(async (response) => {
        const reward = response[0]
        const txnGroup = response[1]
        const myAlgoConnect = new MyAlgoConnect()
        const signedTxnGroup = await myAlgoConnect.signTransaction(txnGroup as AlgorandTxn[])
        const signedTxnGroupStringArray = signedTxnGroup.map((signedTxn) => Buffer.from(signedTxn.blob).toString('base64'))
        txnService.sendTxn(signedTxnGroupStringArray).then(async () => {
          this.$q.notify({
            type: 'positive',
            position: 'bottom',
            message: 'Reward ' + reward + ' EcoRetail Coins sent successfully for purchasing products!'
          })
          this.productForm.id = this.productForm.amount = this.productForm.price = 0
          this.purchaseList = []
          this.wallet = ''
          await this.$store.dispatch('auth/check')
        }).catch(() => {
          this.$q.notify({
            type: 'negative',
            position: 'bottom',
            message: 'Transaction(s) unsuccessful, insufficient funds or permissions or wrong wallet/data!'
          })
        })
      })
    }
  }
})
</script>

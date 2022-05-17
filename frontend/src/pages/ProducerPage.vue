<template>
  <q-page class="row items-center justify-evenly">
      <q-card class="column q-ma-md q-ma-md-lg q-pa-xs q-pa-md-md q-pa-lg-lg flex justify-center" style="width: 550px">
        <q-card-section class="flex justify-center q-pb-xs">
          <div class="text-h5">
            Add new or update existing product
          </div>
        </q-card-section>

        <q-form class="q-gutter-xs" @submit="submitProduct">
          <q-card-section class="q-gutter-y-sm">
            <q-separator class="q-mb-md" />

            <q-input
                    name="name"
                    type="text"
                    v-model="productForm.name"
                    label="Name"
                    :rules="[val => !!val || 'Product name is required!']"
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
                    name="description"
                    type="text"
                    v-model="productForm.description"
                    label="Description"
                    :rules="[val => !!val || 'Product description is required!']"
                    lazy-rules="ondemand"
                    dense
                    filled
                    clearable>
              <template v-slot:prepend>
                <q-icon name="description" />
              </template>
            </q-input>

            <q-select
                    name="rating"
                    type="text"
                    v-model="productForm.rating"
                    :options="options"
                    label="Eco rating category"
                    :rules="[val => !!val || 'Product rating is required!']"
                    lazy-rules="ondemand"
                    dense
                    filled
                    clearable>
              <template v-slot:prepend>
                <q-icon name="description" />
              </template>
            </q-select>

          </q-card-section>

          <q-card-actions class="flex justify-center">
            <q-btn outline rounded color="secondary" size="md" class="full-width q-mb-lg" label="Confirm product data" type="submit" />
          </q-card-actions>
        </q-form>
      </q-card>
  </q-page>
</template>

<script lang="ts">
import MyAlgoConnect, { AlgorandTxn } from '@randlabs/myalgo-connect'
import { defineComponent } from 'vue'
import { mapGetters } from 'vuex'
import { txnService, productService } from '../services'

export default defineComponent({
  name: 'ProducerPage',
  data() {
    return {
      productForm: {
        name: '',
        description: '',
        rating: ''
      },
      options: [
        'A', 'B', 'C', 'D', 'E', 'F'
      ]
    }
  },

  computed: {
    ...mapGetters('auth', {
      getUser: 'getUser'
    })
  },

  methods: {
    async submitProduct() {
      txnService.addProducGetTxn().then(async (txn) => {
        console.log(txn)
        const myAlgoConnect = new MyAlgoConnect()
        const signedTxn = await myAlgoConnect.signTransaction(txn)
        const signedTxnString = Buffer.from(signedTxn.blob).toString('base64')
        txnService.sendTxn(signedTxnString).then((response) => {
          productService.addProduct(this.productForm).then(() => {
            this.$q.notify({
              type: 'positive',
              position: 'bottom',
              message: response
            })
            this.productForm.name = this.productForm.description = this.productForm.rating = ''
          })
        }).catch(() => {
          this.$q.notify({
            type: 'negative',
            position: 'bottom',
            message: 'Transaction(s) unsuccessful, insufficient funds or permissions or wrong wallet!'
          })
        })
      })
    }
  }
})
</script>

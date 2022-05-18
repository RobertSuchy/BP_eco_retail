<template>
  <q-page class="column items-center justify-evenly">
      <q-card class="column q-ma-md q-ma-md-lg q-pa-xs q-pa-md-md q-pa-lg-lg flex justify-center"
      :style="$q.screen.lt.sm ? {'width': '90%'} : $q.screen.lt.md ? {'width': '50%'} : $q.screen.lt.lg ? {'width': '35%'} : {'width': '25%'}">
        <q-card-section class="flex justify-center q-pb-xs">
          <div class="text-h5">
            Add new or update existing product
          </div>
        </q-card-section>

        <q-form class="q-gutter-xs" @submit="submitProduct" >
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

      <q-table
        title="Your products"
        :rows="getProducersProducts(getUser.name)"
        :columns="columns"
        row-key="id"
        :dense="$q.screen.lt.md"
        wrap-cells
        virtual-scroll
        :rows-per-page-options="[0]"
        class="q-ma-md q-ma-md-lg q-pa-xs q-pa-md-md q-pa-lg-lg"
        style="height: 500px"
        :style="$q.screen.lt.sm ? {'width': '90%'} : $q.screen.lt.md ? {'width': '80%'} : $q.screen.lt.lg ? {'width': '70%'} : {'width': '60%'}"
      />
  </q-page>
</template>

<script lang="ts">
import MyAlgoConnect from '@randlabs/myalgo-connect'
import { QTableProps } from 'quasar'
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
      ],
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
      ] as QTableProps['columns']
    }
  },

  computed: {
    ...mapGetters('auth', {
      getUser: 'getUser'
    }),
    ...mapGetters('products', {
      getProducersProducts: 'getProducersProducts'
    })
  },

  methods: {
    async submitProduct() {
      txnService.addProducGetTxn().then(async (txn) => {
        const myAlgoConnect = new MyAlgoConnect()
        const signedTxn = await myAlgoConnect.signTransaction(txn)
        const signedTxnString = Buffer.from(signedTxn.blob).toString('base64')
        txnService.sendTxn(signedTxnString).then(() => {
          productService.addProduct(this.productForm).then(async (created) => {
            this.$q.notify({
              type: 'positive',
              position: 'bottom',
              message: created ? 'Product successfully added!' : 'Product successfully updated!'
            })
            this.productForm.name = this.productForm.description = this.productForm.rating = ''
            await this.$store.dispatch('auth/check')
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

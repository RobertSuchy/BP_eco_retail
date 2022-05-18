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
        style="height: 75vh"
        :style="$q.screen.lt.sm ? {'width': '90%'} : $q.screen.lt.md ? {'width': '80%'} : $q.screen.lt.lg ? {'width': '70%'} : {'width': '60%'}"
      />
  </q-page>
</template>

<script lang="ts">
// import MyAlgoConnect from '@randlabs/myalgo-connect'
import { QTableProps } from 'quasar'
import { defineComponent } from 'vue'
import { mapGetters } from 'vuex'
// import { txnService, productService } from '../services'

export default defineComponent({
  name: 'ProductsPage',
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
      ] as QTableProps['columns']
    }
  },

  computed: {
    ...mapGetters('auth', {
      getUser: 'getUser'
    }),
    ...mapGetters('products', {
      getAllProducts: 'getAllProducts'
    })
  },

  methods: {
    // async submitProduct() {
    //   txnService.addProducGetTxn().then(async (txn) => {
    //     const myAlgoConnect = new MyAlgoConnect()
    //     const signedTxn = await myAlgoConnect.signTransaction(txn)
    //     const signedTxnString = Buffer.from(signedTxn.blob).toString('base64')
    //     txnService.sendTxn(signedTxnString).then(() => {
    //       productService.addProduct(this.productForm).then(async (created) => {
    //         this.$q.notify({
    //           type: 'positive',
    //           position: 'bottom',
    //           message: created ? 'Product successfully added!' : 'Product successfully updated!'
    //         })
    //         this.productForm.name = this.productForm.description = this.productForm.rating = ''
    //         await this.$store.dispatch('auth/check')
    //       })
    //     }).catch(() => {
    //       this.$q.notify({
    //         type: 'negative',
    //         position: 'bottom',
    //         message: 'Transaction(s) unsuccessful, insufficient funds or permissions or wrong wallet!'
    //       })
    //     })
    //   })
    // }
  }
})
</script>

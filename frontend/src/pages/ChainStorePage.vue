<template>
  <q-page class="row items-center justify-evenly">
      <q-card class="column q-ma-md q-ma-md-lg q-pa-xs q-pa-md-md q-pa-lg-lg flex justify-center" style="width: 550px">
        <q-card-section class="flex justify-center q-pb-md">
          <div class="text-h5">
            Exchange
          </div>
        </q-card-section>

        <q-form class="q-gutter-md" @submit.prevent="submitExchange">
          <q-card-section class="q-gutter-y-lg">
            <q-separator/>

            <q-input
                    name="amount"
                    type="number"
                    v-model="amount"
                    label="Amount"
                    hint="1 EcoRetail Coin = 0.01 Algos"
                    dense
                    filled
                    clearable
                    autofocus>
              <template v-slot:prepend>
                <q-icon name="eco" color="green" />
              </template>
            </q-input>

            <div class="row">
              <div class="col-6">
                <q-field borderless label="Cost Algos:" stack-label class="full-width">
                  <template v-slot:prepend>
                  <q-icon name="account_balance_wallet" />
                  </template>
                  <template v-slot:control>
                  <div class="self-center full-width no-outline text-subtitle1">{{ amount / 100 }}</div>
                  </template>
                </q-field>

              </div>
              <div class="col-6">
                <q-field borderless label="Algos available:" stack-label class="full-width">
                    <template v-slot:prepend>
                    <q-icon name="account_balance_wallet" />
                    </template>
                    <template v-slot:control>
                    <div class="self-center full-width no-outline text-subtitle1">{{ getUser.algos }}</div>
                    </template>
                </q-field>

              </div>

            </div>
          </q-card-section>

          <q-card-actions class="flex justify-center q-gutter-md q-mt-xs">
            <q-btn outline rounded color="secondary" size="md" class="full-width q-mb-lg" label="Buy EcoRetail Coins" type="submit" />
          </q-card-actions>
        </q-form>
      </q-card>
  </q-page>
</template>

<script lang="ts">
import MyAlgoConnect, { AlgorandTxn } from '@randlabs/myalgo-connect'
import { defineComponent } from 'vue'
import { mapGetters } from 'vuex'
import { txnService } from '../services'

export default defineComponent({
  name: 'ChainStorePage',
  data() {
    return {
      amount: 0
    }
  },

  computed: {
    ...mapGetters('auth', {
      getUser: 'getUser'
    })
  },

  methods: {
    async submitExchange() {
      if (this.amount <= 0) {
        this.$q.notify({
          type: 'negative',
          position: 'bottom',
          message: 'Amount must be greater than 0!'
        })
      }
      txnService.buyEcoCoinsGetTxn(this.amount).then(async (txnGroup) => {
        const myAlgoConnect = new MyAlgoConnect()
        const signedTxnGroup = await myAlgoConnect.signTransaction(txnGroup as AlgorandTxn[])
        const signedTxnGroupStringArray = signedTxnGroup.map((signedTxn) => Buffer.from(signedTxn.blob).toString('base64'))
        txnService.sendTxn(signedTxnGroupStringArray).then((response) => {
          this.$q.notify({
            type: 'positive',
            position: 'bottom',
            message: response
          })
        }).catch(() => {
          this.$q.notify({
            type: 'negative',
            position: 'bottom',
            message: 'Transaction(s) unsuccessful, insufficient funds or wrong wallet!'
          })
        })
      })
      this.$forceUpdate()
    }
  }
})
</script>

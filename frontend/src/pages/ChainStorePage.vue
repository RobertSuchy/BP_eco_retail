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
                    hint="1 EcoRetail Coin = 0.01 ALGOs"
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

            <!-- <q-field borderless label="ALGOs:" stack-label>
                <template v-slot:prepend>
                <q-icon name="account_balance_wallet" />
                </template>
                <template v-slot:control>
                <div class="self-center full-width no-outline text-subtitle1">{{ getUser.algos }}</div>
                </template>
            </q-field>

            <q-field borderless label="EcoRetail Coins:" stack-label>
                <template v-slot:prepend>
                <q-icon name="eco" color="green" />
                </template>
                <template v-slot:control>
                <div class="self-center full-width no-outline text-green text-subtitle1">{{ getUser.ecoCoins }}</div>
                </template>
            </q-field> -->
      </q-card>
  </q-page>
</template>

<script lang="ts">
import MyAlgoConnect from '@randlabs/myalgo-connect'
import cloneDeep from 'lodash/cloneDeep'
import { defineComponent } from 'vue'
import { mapGetters } from 'vuex'
import { txnService } from '../services'

export default defineComponent({
  name: 'ChainStore',
  data() {
    return {
      amount: 0
    }
  },

  computed: {
    ...mapGetters('auth', {
      getUser: 'getUser',
      getMyAlgoConnect: 'getMyAlgoConnect'
    })
  },

  methods: {
    submitExchange() {
      txnService.buyEcoCoinsGetTxn(this.getUser.wallet, this.amount).then(async (txnGroup) => {
        console.log('----------------')
        console.log(txnGroup)
        // const myAlgoConnect = cloneDeep(this.getMyAlgoConnect)
        const myAlgoConnect = new MyAlgoConnect()
        console.log(myAlgoConnect)
        const signedTxnGroup = await myAlgoConnect.signTransaction(txnGroup)
        console.log('----------------')
        console.log(signedTxnGroup)
      })
    }
  }
})
</script>

<style scoped>
  .wallet-address {
    font-size: 8px
  }
@media (min-width: 576px) {
  .wallet-address {
    font-size: 14px
  }
}
</style>

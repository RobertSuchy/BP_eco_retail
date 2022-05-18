<template>
  <q-page class="row items-center justify-evenly">
      <q-card class="column q-ma-md q-ma-md- q-pa-xs q-pa-md-md q-pa-lg-lg flex justify-center" style="width: 675px">
        <q-card-section class="flex justify-center q-pb-xs">
          <div class="text-h5">
            Account information
          </div>
        </q-card-section>

        <q-card-section class="q-gutter-y-md">
          <q-separator/>

          <q-field borderless label="Email:" stack-label>
              <template v-slot:prepend>
              <q-icon name="email" />
              </template>
              <template v-slot:control>
              <div class="self-center full-width no-outline text-subtitle1">{{ getUser.email }}</div>
              </template>
          </q-field>

          <q-field borderless label="User type:" stack-label>
              <template v-slot:prepend>
              <q-icon name="person" />
              </template>
              <template v-slot:control>
              <div class="self-center full-width no-outline text-subtitle1">{{ getUser.userType }}</div>
              </template>
          </q-field>

          <q-field v-if="getUser.userType == 'chainStore' || getUser.userType == 'producer'" borderless label="Name:" stack-label>
              <template v-slot:prepend>
              <q-icon name="label" />
              </template>
              <template v-slot:control>
              <div class="self-center full-width no-outline text-subtitle1">{{ getUser.name }}</div>
              </template>
          </q-field>

          <q-field borderless label="Wallet address:" stack-label>
              <template v-slot:prepend>
              <q-icon name="wallet" />
              </template>
              <template v-slot:control>
              <div class="self-center full-width no-outline wallet-address">{{ getUser.wallet }}</div>
              </template>
          </q-field>

          <q-field borderless label="Algos:" stack-label>
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
          </q-field>
        </q-card-section>

        <q-card-section v-if="getUser.userType === 'chainStore'">
          <q-form class="q-gutter-md" @submit.prevent="submitRewardsPolicy">
            <div class="text-h6">
              Rewards policy (% reward for products in each category)
            </div>
            <div class="row q-gutter-sm">
              <q-input
                      name="category_a"
                      v-model="rewardsPolicyForm.categoryA"
                      label="A"
                      dense
                      filled>
              </q-input>

              <q-input
                      name="amount"
                      v-model="rewardsPolicyForm.categoryB"
                      label="B"
                      dense
                      filled>
              </q-input>

              <q-input
                      name="amount"
                      v-model="rewardsPolicyForm.categoryC"
                      label="C"
                      dense
                      filled>
              </q-input>

              <q-input
                      name="amount"
                      v-model="rewardsPolicyForm.categoryD"
                      label="D"
                      dense
                      filled>
              </q-input>

              <q-input
                      name="amount"
                      v-model="rewardsPolicyForm.categoryE"
                      label="E"
                      dense
                      filled>
              </q-input>

              <q-input
                      name="amount"
                      v-model="rewardsPolicyForm.categoryF"
                      label="F"
                      dense
                      filled>
              </q-input>

              <q-btn outline rounded color="secondary" size="md" class="full-width q-mt-lg" label="Update rewards policy" type="submit" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
  </q-page>
</template>

<script lang="ts">
import { RewardsPolicy } from '../contracts'
import { defineComponent } from 'vue'
import { mapGetters } from 'vuex'
import { productService } from '../services'

export default defineComponent({
  name: 'MyAccountPage',
  data() {
    return {
      rewardsPolicyForm: {
        categoryA: 0,
        categoryB: 0,
        categoryC: 0,
        categoryD: 0,
        categoryE: 0,
        categoryF: 0
      }
    }
  },

  mounted() {
    const rewardsPolicy = this.$store.state.auth.rewardsPolicy
    if (rewardsPolicy) {
      this.rewardsPolicyForm.categoryA = rewardsPolicy.categoryA
      this.rewardsPolicyForm.categoryB = rewardsPolicy.categoryB
      this.rewardsPolicyForm.categoryC = rewardsPolicy.categoryC
      this.rewardsPolicyForm.categoryD = rewardsPolicy.categoryD
      this.rewardsPolicyForm.categoryE = rewardsPolicy.categoryE
      this.rewardsPolicyForm.categoryF = rewardsPolicy.categoryF
    }
  },

  computed: {
    ...mapGetters('auth', {
      getUser: 'getUser'
    })
  },

  methods: {
    async submitRewardsPolicy() {
      const form = this.rewardsPolicyForm
      if (form.categoryA > form.categoryB && form.categoryB > form.categoryC && form.categoryC > form.categoryD && form.categoryD > form.categoryE && form.categoryE > form.categoryF) {
        productService.updateRewardsPolicy(this.rewardsPolicyForm).then(() => {
          this.$q.notify({
            type: 'positive',
            position: 'bottom',
            message: 'Updated successfully!'
          })
        }).catch(() => {
          this.$q.notify({
            type: 'negative',
            position: 'bottom',
            message: 'Update failed!'
          })
        })
      } else {
        this.$q.notify({
          type: 'negative',
          position: 'bottom',
          message: 'Invalid input!'
        })
      }
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

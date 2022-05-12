<template>
  <q-page class="row items-center justify-evenly">
    <div class="q-gutter-lg">
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

      <q-field borderless label="Wallet address:" stack-label>
        <template v-slot:prepend>
          <q-icon name="wallet" />
        </template>
        <template v-slot:control>
          <div class="self-center full-width no-outline wallet-address">{{ getUser.wallet }}</div>
        </template>
      </q-field>

      <q-field borderless label="ALGOs:" stack-label>
        <template v-slot:prepend>
          <q-icon name="account_balance_wallet" />
        </template>
        <template v-slot:control>
          <div class="self-center full-width no-outline text-subtitle1">{{ getUser.algos }}</div>
        </template>
      </q-field>

      <q-field borderless label="EcoRetail tokens:" stack-label>
        <template v-slot:prepend>
          <q-icon name="eco" color="green" />
        </template>
        <template v-slot:control>
          <div class="self-center full-width no-outline text-green text-subtitle1">{{ getUser.ecoTokens }}</div>
        </template>
      </q-field>
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'CustomerPage',
  data() {
    return {

    }
  },

  computed: {
    ...mapGetters('auth', {
      getUser: 'getUser'
    })
  },

  methods: {
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

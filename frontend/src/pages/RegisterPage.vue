<template>
  <q-page class="row items-center justify-evenly">
    <q-card class="q-ma-lg q-pa-lg" style="width: 450px">
      <q-card-section class="flex justify-center">
        <div class="text-h4">
          Register
        </div>
      </q-card-section>
      <q-form class="q-gutter-md" @submit.prevent="submitRegForm">
        <q-card-section class="q-gutter-y-lg">
          <q-input
                  name="email"
                  type="email"
                  v-model="regForm.email"
                  label="Email"
                  dense
                  filled
                  clearable
                  autofocus>
            <template v-slot:prepend>
              <q-icon name="email" />
            </template>
          </q-input>

          <q-input
                  name="password"
                  :type="passwordVisible ? 'text' : 'password'"
                  v-model="regForm.password"
                  label="Password"
                  dense
                  filled
                  clearable
                  autocomplete>
            <template v-slot:prepend>
              <q-icon name="lock" />
            </template>
            <template v-slot:append>
            <q-icon
              :name="passwordVisible ? 'visibility' : 'visibility_off'"
              class="cursor-pointer"
              @click="passwordVisible = !passwordVisible"
            />
            </template>
          </q-input>

          <q-input
                  name="password_confirmation"
                  :type="passwordVisible ? 'text' : 'password'"
                  v-model="regForm.passwordConfirmation"
                  label="Confirm password"
                  dense
                  filled
                  clearable
                  autocomplete>
            <template v-slot:prepend>
              <q-icon name="lock" />
            </template>
            <template v-slot:append>
            <q-icon
              :name="passwordVisible ? 'visibility' : 'visibility_off'"
              class="cursor-pointer"
              @click="passwordVisible = !passwordVisible"
            />
            </template>
          </q-input>

          <div class="row">
            Choose an appropriate user type for you:
            <div class="q-gutter-md">
              <q-radio name="user_type" v-model="regForm.userType" val="customer" label="Customer" />
              <q-radio name="user_type" v-model="regForm.userType" val="chainStore" label="Chain store" />
              <q-radio name="user_type" v-model="regForm.userType" val="producer" label="Producer" />
            </div>
          </div>
        </q-card-section>

        <q-card-actions class="flex justify-center q-gutter-md q-mt-xs">
          <q-btn outline rounded color="secondary" size="md" class="full-width q-mb-lg" label="Register" type="submit" />
          Already have an account?
          <q-btn outline rounded size="md" class="full-width" label="Login" :to="{ name:'login' }" />
        </q-card-actions>
      </q-form>
    </q-card>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import MyAlgoConnect from '@randlabs/myalgo-connect'
import { txnService } from '../services'

export default defineComponent({
  name: 'RegisterPage',
  data() {
    return {
      regForm: {
        email: '',
        userType: '',
        wallet: '',
        password: '',
        passwordConfirmation: ''
      },
      passwordVisible: false
    }
  },
  methods: {
    async submitRegForm() {
      if (!this.regForm.email) {
        this.$q.notify({
          type: 'negative',
          position: 'bottom',
          message: 'Email is required!'
        })
      } else if (!this.regForm.userType) {
        this.$q.notify({
          type: 'negative',
          position: 'bottom',
          message: 'User type is required!'
        })
      } else if (!this.regForm.password || !this.regForm.passwordConfirmation) {
        this.$q.notify({
          type: 'negative',
          position: 'bottom',
          message: 'Password is required!'
        })
      } else if (this.regForm.password !== this.regForm.passwordConfirmation) {
        this.$q.notify({
          type: 'negative',
          position: 'bottom',
          message: 'Passwords do not match!'
        })
      } else {
        const myAlgoConnect = new MyAlgoConnect()
        const accountsSharedByUser = await myAlgoConnect.connect()
        this.regForm.wallet = accountsSharedByUser[0].address
        this.optInAsset(myAlgoConnect).then((result) => {
          if (result) {
            this.optInContract(myAlgoConnect).then((result) => {
              if (result) {
                this.$store.dispatch('auth/register', this.regForm).then((user) => {
                  if (user) {
                    this.$q.notify({
                      type: 'positive',
                      position: 'bottom',
                      message: 'Registration successful!'
                    })
                    this.$router.push({ name: 'login' })
                  }
                }).catch(() => {
                  this.$q.notify({
                    type: 'negative',
                    position: 'bottom',
                    message: 'Registration unsuccessful! Email or wallet already used!'
                  })
                })
              }
            })
          }
        })
      }
    },

    async optInAsset(myAlgoConnect: MyAlgoConnect): Promise<boolean | undefined> {
      const data = {
        wallet: this.regForm.wallet
      }
      return txnService.optInAssetGetTxn(JSON.stringify(data)).then(async (txn) => {
        if (!txn) {
          this.$q.notify({
            type: 'positive',
            position: 'bottom',
            message: 'You have already added our EcoRetail token to your Algorand wallet!'
          })
          return true
        }

        const signedTxn = await myAlgoConnect.signTransaction(txn)
        return txnService.optInSendTxn(Buffer.from(signedTxn.blob).toString('base64')).then((response) => {
          if (response === 'err') {
            this.$q.notify({
              type: 'negative',
              position: 'bottom',
              message: 'You need at least 1000 microAlgos to opt-in our EcoRetail token!'
            })
            return false
          }

          this.$q.notify({
            type: 'positive',
            position: 'bottom',
            message: 'Successfully added our EcoRetail token to your Algorand wallet!'
          })
          return true
        })
      })
    },

    async optInContract(myAlgoConnect: MyAlgoConnect): Promise<boolean | undefined> {
      const data = {
        wallet: this.regForm.wallet,
        user_type: this.regForm.userType
      }
      return txnService.optInContractGetTxn(JSON.stringify(data)).then(async (txn) => {
        if (!txn) {
          this.$q.notify({
            type: 'positive',
            position: 'bottom',
            message: 'You have already opted-in our EcoRetail smart contract!'
          })
          return true
        }

        const signedTxn = await myAlgoConnect.signTransaction(txn)
        return txnService.optInSendTxn(Buffer.from(signedTxn.blob).toString('base64')).then((response) => {
          if (response === 'err') {
            this.$q.notify({
              type: 'negative',
              position: 'bottom',
              message: 'You need at least 1000 microAlgos to opt-in our smart contract!'
            })
            return false
          }

          this.$q.notify({
            type: 'positive',
            position: 'bottom',
            message: 'Successfully opted-in our smart contract, now you are ready to register and use our application!'
          })
          return true
        })
      })
    }
  }
})
</script>

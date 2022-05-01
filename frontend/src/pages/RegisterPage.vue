<template>
  <q-page class="row items-center justify-evenly">
    <q-card class="q-ma-lg q-pa-lg" style="width: 450px">
      <q-card-section class="flex justify-center">
        <div class="text-h4">
          Register
        </div>
      </q-card-section>
      <q-form class="q-gutter-md">
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
          <q-btn outline rounded color="secondary" size="md" class="full-width q-mb-lg" label="Register" @click="submitRegForm" />
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
        password: '',
        passwordConfirmation: '',
        userType: '',
        wallet: ''
      },
      passwordVisible: false
    }
  },
  methods: {
    async submitRegForm() {
      const myAlgoConnect = new MyAlgoConnect()
      const accountsSharedByUser = await myAlgoConnect.connect()
      this.regForm.wallet = accountsSharedByUser[0].address
      txnService.optIn(this.regForm.wallet)
      // this.$store.dispatch('auth/register', this.regForm).then(() => this.$router.push({ name: 'login' }))
    }
  }
})
</script>

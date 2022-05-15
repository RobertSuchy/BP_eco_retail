<template>
  <q-page class="row items-center justify-evenly">
    <q-card class="q-ma-md q-ma-md-lg q-pa-xs q-pa-md-md q-pa-lg-lg" style="width: 450px">
      <q-card-section class="flex justify-center">
        <div class="text-h4">
          Login
        </div>
      </q-card-section>
      <q-form class="q-gutter-md" @submit.prevent="submitLoginForm">
        <q-card-section class="q-gutter-y-lg">
          <q-input
                  name="email"
                  type="email"
                  v-model="loginForm.username"
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
                  v-model="loginForm.password"
                  label="Password"
                  dense
                  filled
                  clearable>
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
        </q-card-section>

        <q-card-actions class="flex justify-center q-gutter-md q-mt-xs">
          <q-btn outline rounded color="secondary" size="md" class="full-width q-mb-lg" label="Login" type="submit" />
          Don't have an account?
          <q-btn outline rounded size="md" class="full-width" label="Register" :to="{ name:'register' }" />
        </q-card-actions>
      </q-form>
    </q-card>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import MyAlgoConnect from '@randlabs/myalgo-connect'

export default defineComponent({
  name: 'LoginPage',
  data() {
    return {
      loginForm: {
        // field username contains email (Django rest_framework.authtoken requires username)
        username: '',
        password: ''
      },
      wallet: '',
      passwordVisible: false
    }
  },
  methods: {
    async submitLoginForm() {
      if (!this.loginForm.username) {
        this.$q.notify({
          type: 'negative',
          position: 'bottom',
          message: 'Email is required!'
        })
      } else if (!this.loginForm.password) {
        this.$q.notify({
          type: 'negative',
          position: 'bottom',
          message: 'Password is required!'
        })
      } else {
        const myAlgoConnect = new MyAlgoConnect({ timeout: 30000 })
        const accountsSharedByUser = await myAlgoConnect.connect()
        this.wallet = accountsSharedByUser[0].address
        this.$store.dispatch('auth/login', { credentials: this.loginForm, wallet: this.wallet, myAlgoConnect }).then((apiToken) => {
          if (apiToken) {
            this.$q.notify({
              type: 'positive',
              position: 'bottom',
              message: 'Login successful!'
            })
            this.$router.push({ name: 'myAccount' })
          }
        }).catch(() => {
          this.$q.notify({
            type: 'negative',
            position: 'bottom',
            message: 'Login unsuccessful! Check your login credentials!'
          })
        })
      }
    }
  }
})
</script>

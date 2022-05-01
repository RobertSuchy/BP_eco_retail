<template>
  <q-page class="row items-center justify-evenly">
    <q-card class="q-ma-lg q-pa-lg" style="width: 450px">
      <q-card-section class="flex justify-center">
        <div class="text-h4">
          Login
        </div>
      </q-card-section>
      <q-form class="q-gutter-md" @submit.prevent="submitRegistration">
        <q-card-section class="q-gutter-y-lg">
          <q-input
                  name="email"
                  type="email"
                  v-model="loginForm.email"
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
          <q-btn outline rounded color="secondary" size="md" class="full-width q-mb-lg" label="Login" @click="submitLoginForm" />
          Don't have an account?
          <q-btn outline rounded size="md" class="full-width" label="Register" :to="{ name:'register' }" />
        </q-card-actions>
      </q-form>
    </q-card>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'LoginPage',
  data() {
    return {
      loginForm: {
        email: '',
        password: '',
        passwordConfirmation: '',
        userType: ''
      },
      passwordVisible: false
    }
  },
  methods: {
    submitLoginForm() {
      this.$store.dispatch('auth/register', this.loginForm).then(() => this.$router.push({ name: 'login' }))
    }
  }
})
</script>

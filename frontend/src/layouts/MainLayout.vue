<template>
  <q-layout view="hHh lpR fff">

    <q-header elevated class="bg-green-10 text-white" height-hint="98">
      <q-toolbar class="flex">
        <q-toolbar-title>
          <q-avatar>
            <q-icon name="eco" color="green" size="30px" />
          </q-avatar>
          EcoRetail
        </q-toolbar-title>

        <q-toggle v-model="dark" color="green" />
        <q-btn v-if="isAuthenticated" round icon="logout" @click="logout" />
      </q-toolbar>

      <q-tabs class="bg-green-9" align="left">
        <q-route-tab :to="{ name: 'home' }" label="Home" />
        <q-route-tab v-if="!isAuthenticated" :to="{ name: 'login' }" label="Login" />
        <q-route-tab v-if="!isAuthenticated" :to="{ name: 'register' }" label="Register" />
        <q-route-tab v-if="isAuthenticated" :to="{ name: 'myAccount' }" label="My account" />
        <q-route-tab v-if="isAuthenticated" :to="{ name: 'allProducts' }" label="All products" />
        <q-route-tab v-if="isAuthenticated && getUser.userType === 'chainStore'" :to="{ name: 'chainStore' }" label="Manage tokens" />
        <q-route-tab v-if="isAuthenticated && getUser.userType === 'producer'" :to="{ name: 'producer' }" label="Manage products" />
      </q-tabs>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer elevated class="bg-blue-grey-10 text-white">
      <q-toolbar class="column">
        <q-toolbar-title class="q-mt-md">
          <q-avatar>
            <q-icon name="eco" color="green" size="30px" />
          </q-avatar>
          EcoRetail
        </q-toolbar-title>
        <div>
          Róbert Suchý
        </div>
        <div>
          Supervisor: Ing. Lukáš Mastiľak
        </div>
        <div>
          Consultant: Ing. Kristián Košťál, PhD.
        </div>
        <div class="q-mb-md">
          BP 2021/2022
        </div>
      </q-toolbar>
    </q-footer>

  </q-layout>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      dark: true
    }
  },

  watch: {
    dark: function() {
      this.$q.dark.set(this.dark)
    }
  },

  computed: {
    ...mapGetters('auth', {
      isAuthenticated: 'isAuthenticated',
      getUser: 'getUser'
    })
  },

  methods: {
    logout() {
      this.$store.dispatch('auth/logout').then(() => this.$router.push({ name: 'home' }))
    }
  }
}
</script>

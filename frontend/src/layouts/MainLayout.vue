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

        <q-btn v-if="isAuthenticated" round icon="logout" @click="logout" />
      </q-toolbar>

      <q-tabs class="bg-green-9" align="left">
        <q-route-tab :to="{ name:'home' }" label="Home" />
        <q-route-tab v-if="!isAuthenticated" :to="{ name:'login' }" label="Login" />
        <q-route-tab v-if="!isAuthenticated" :to="{ name:'register' }" label="Register" />
        <q-route-tab v-if="isAuthenticated" :to="{ name:'user' }" label="My account" />
        <q-route-tab v-if="isAuthenticated && getUser.userType === 'customer'" :to="{ name:'user' }" label="test" />
      </q-tabs>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer elevated class="bg-blue-grey-10 text-white">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <q-icon name="eco" color="green" size="30px" />
          </q-avatar>
          EcoRetail
        </q-toolbar-title>
        Róbert Suchý | Lukáš Mastiľak | BP 2021/2022
      </q-toolbar>
    </q-footer>

  </q-layout>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
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

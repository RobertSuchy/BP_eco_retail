<template>
  <q-layout view="hHh lpR fff">

    <q-header elevated class="bg-primary text-white" height-hint="98">
      <q-toolbar class="flex">
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <q-avatar>
            <q-icon name="eco" color="green" size="30px" />
          </q-avatar>
          EcoRetail
        </q-toolbar-title>

        <q-btn round icon="logout" @click="logout" />
      </q-toolbar>

      <!-- <q-tabs align="left">
        <q-route-tab to="/page1" label="Page One" />
        <q-route-tab to="/page2" label="Page Two" />
        <q-route-tab to="/page3" label="Page Three" />
      </q-tabs> -->

    </q-header>

    <q-drawer show-if-above v-model="leftDrawerOpen" side="left" bordered>
      <!-- drawer content -->
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer elevated class="bg-grey-8 text-white">
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
import { ref } from 'vue'

export default {
  setup () {
    const leftDrawerOpen = ref(false)

    return {
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('auth/logout').then(() => this.$router.push({ name: 'home' }))
    }
  }
}
</script>

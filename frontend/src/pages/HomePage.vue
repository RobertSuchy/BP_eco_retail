<template>
  <q-page class="row items-center justify-evenly">
    <q-card class="q-ma-md q-ma-md-lg q-pa-xs q-pa-md-md q-pa-lg-lg" style="width: 550px">
      <q-card-section class="flex justify-center">
        <div class="text-h4">
          Welcome to EcoRetail App!
        </div>
      </q-card-section>
      <q-card-section class="flex justify-center">
        <div class="text-h6 q-mb-md">
          Enter the register page, if you want to discover functionalities of our prototype.
        </div>
        <div class="text-h6">
          If you alreade have an account, please choose the login page.
        </div>

      </q-card-section>
    </q-card>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HomePage',
  data() {
    return {};
  }
});
</script>

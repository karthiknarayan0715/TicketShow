<script>
import { useCookies } from 'vue3-cookies';

export default {
  mounted() {
      console.log(this.$login.verify())
      if(!this.$login.verify()) this.$router.push("/login")
  }
}
</script>

<template>
    <div class="about">
      <h1>This is an Home page</h1>
    </div>
  </template>
  
  <style>
  </style>
  
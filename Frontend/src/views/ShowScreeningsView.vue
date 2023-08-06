<script>
import {useCookies} from "vue3-cookies"
export default {
    data() {
        return {
          user: null,
          admin: false,
          edit: false,
          OverlayOpen: false,
          show_id: this.$route.query.id
        }
    },
    async mounted(){
      if(!this.$login.verify()){
        this.$router.push("/login")
        this.$toast.show("400", "Not logged in or session expired")
      }
      this.jwt = this.$login.verify()
      this.user = await this.$login.getUserData();
      this.admin = this.user.role == "admin"
    },
    methods: {
      
    },
    computed: {

    },
    components: {  }
};
</script>

<template>
  <main>
    <div class="main">

    </div>
  </main>
</template>

<style scoped>
.main{
  width: 100%;
  height: 100%;
}
</style>
<script>
import ToastMessage from '../components/ToastMessage.vue';
import { useCookies } from 'vue3-cookies';
export default {
    data() {
        return {
            id: this.$route.query.id,
            loading: false,
            approved: null,
            results: null,
            ticket: null
        };
    },
    async mounted(){
      if(!this.$login.verify()){
        this.$router.push("/")
        this.$toast.show("200", "Login first!")
      }
      this.jwt = this.$login.verify()
      this.user = await this.$login.getUserData();
      if(this.user.role !== "admin"){
        this.$toast.show("403", "Access denied")
        this.$router.push("/")
      }
      this.loading = true
      await this.GetTicketData()
      this.loading = false
    },
    methods: {
      async GetTicketData(){
        let req = {
              "method": "GET",
              headers: {
                  'Content-Type': 'application/json',
                  'Authorization': 'Bearer '+ this.jwt
              }
            }
        let res = await fetch(`${import.meta.env.VITE_APP_BACKEND_URL}/tickets/get?jwt=${this.jwt}&ticket_id=${this.id}`, req)
        let data = await res.json()
        if(res.status == 200){
          this.ticket = data
          this.approved = true
        }
        else{
          this.approved = false
        }

      }
    },
    components: {  }
};
</script>

<template>
  <main>
    <div class="main" v-if="!loading">
      <div class="box" v-if="approved">
        <div class="approved" >Ticket Approved!</div>
        <div class="show-name">{{ ticket.screening.show.name }} @ {{ ticket.screening.venue.name }}</div>
        <div class="admit">
          {{ ticket.quantity }} tickets booked
        </div>
      </div>
      <div class="disapproved" v-else>Ticket approval failed! Ticket not found or cancelled</div>
    </div>
    <div class="loading" v-else>Loading</div>
  </main>
</template>

<style scoped>
.loading{
  width: 100%;
  height: 100%;
  display: flex;
  background-color: rgba(0, 0, 0, 0.3);
  justify-content: center;
  align-items: center;
}
.main{
  width: calc(100% - 60px);
  height: calc(100% - 60px);
  padding: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.box{
  width: 60%;
  height: 80%;
  background-color: #845EC2;
  display: flex;
  flex-direction: column;
}
.approved{
  margin-top: 15px;
  margin-bottom: 15px;
  color: #FFC75F;
  width: 100%;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 25px;
  font-weight: 800;
}
.show-name{
  width: 100%;
  height: 50px;
  margin-top: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #F9F871;
  font-size: 36px;
  font-weight: 800;
}
.admit{
  width: 100%;
  margin: auto;
  color: #FBEAFF;
  font-size: 40px;
  font-weight: 800;
}
</style>
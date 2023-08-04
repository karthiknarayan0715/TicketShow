<script>
import ScreeningsBox from '../components/ScreeningsBox.vue';
import {useCookies} from "vue3-cookies"
export default {
    data() {
        return {
          screening_id: this.$route.query.id,
          ticket_count: 0,
          screening: null,
          venue: null,
          show: null,
          loaded: false,
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
      await this.GetScreening()
    },
    methods: {
      async GetScreening(){
        let req = {
          "method": "GET",
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ this.jwt
          },
        }
        let res = await fetch(import.meta.env.VITE_APP_BACKEND_URL + `/screenings/get?jwt=${this.jwt}&id=${this.screening_id}`, req)
        let data = await res.json()
        this.screening = data
        this.GetVenue()
      },
      async GetVenue(){
        let venue_id = this.screening.venue_id
        let req = {
          "method": "GET",
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ this.jwt
          },
        }
        let res = await fetch(import.meta.env.VITE_APP_BACKEND_URL + `/venues/get?jwt=${this.jwt}&id=${venue_id}`, req)
        let data = await res.json()
        this.venue = data

        this.GetShow()
      },
      async GetShow() {
        let show_id = this.screening.show_id
        let req = {
          "method": "GET",
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ this.jwt
          },
        }
        let res = await fetch(import.meta.env.VITE_APP_BACKEND_URL + `/shows/get?jwt=${this.jwt}&id=${show_id}`, req)
        let data = await res.json()
        this.show = data

        this.loaded = true
      }
    },
    computed: {
      
    },
};
</script>

<template>
  <main>
    <div class="container" v-if="loaded">
      <div class="split desc">
        <div class="show">
          <div class="name">{{ show.name }}</div>
          <div class="duration">{{ show.duration }}</div>
          <div class="desc">{{ show.desc }}</div>
          <div class="rating">{{ show.rating }}</div>
        </div>
        <div class="sep">
          @
        </div>
        <div class="venue">
          <div class="name">{{ venue.name }}</div>
          <div class="place">{{ venue.place }}</div>
          <div class="location">{{ venue.location }}</div>
        </div>
        <div class="available">ONLY {{ screening.available }} TICKETS LEFT!!!</div>
        <div class="book-section">
          <div class="button decrement" @click="()=>{
            if(this.ticket_count > 0)
              this.ticket_count -= 1
          }">-</div>
          <input class="ticket-count" type="text" v-model="ticket_count" disabled>
          <div class="button increment" @click="()=>{
            if(this.ticket_count < screening.available)
              this.ticket_count += 1
          }">+</div>
          <div class="book">Book!</div>
        </div>
      </div>
      <div class="split ticket">

      </div>
    </div>
    <div class="container" v-else>Loading...</div>
  </main>
</template>

<style scoped>
.main{
  width: 100%;
  height: 100%;
}
.container{
  width: 100%;
  height: 100%;
  display: flex;
}
.split{
  padding-top: 40px;
  width: 50%;
  height: calc(100% - 40px);
  display: flex;
  flex-direction: column;
  align-items: center;
}
.show{
  width: 100%;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.show .name{
  font-size: 24px;
  font-weight: 800;
  color: #F9F871;
}
.show .desc{
  margin-top: 10px;
  width: 400px; 
  font-size: 16px;
  color: #FBEAFF;
}
.show .duration{
  color: #FFC75F;
  font-size: 13px;
}
.show .rating{
  color: #e8c37e;
  font-size: 26px;
}
.sep{
  margin-top: 40px;
  margin-bottom: 40px;
  color: #dfcce3;
}
.venue{
  width: 100%;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.venue .name{
  font-size: 24px;
  font-weight: 800;
  color: #F9F871;
}
.venue .place{
  color: #FFC75F;
  font-size: 13px;
}
.venue .location{
  color: white;
  font-size: 16px;
  margin-top: 15px;
}
.available{
  color: #9cc25e;
  margin: auto;
  font-size: 24px;
  font-weight: 800;
}
.book-section{
  width: 100%;
  height: 80px;
  display: flex;
  align-items: center;
  background-color: #4e84974d;
}
.ticket-count{
  width: 100px;
  height: 50px;
  text-align: center;
  font-size: 24px;
}
.book{
  width: 100px;
  height: 50px;
  background-color: #FF9671;
  border-radius: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  cursor: pointer;
  transition-duration: 100ms;
  margin-left: auto;
  margin-right: 40px;
}
.book:hover{
  background-color: #e28d6d;
}
.button{
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition-duration: 100ms;
  background-color: #FF6F91;
}
.button:hover{
  background-color: #e8718d;
}
.button.decrement{
  margin-left: 40px;
}
</style>
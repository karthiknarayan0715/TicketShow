<script>
import {useCookies} from "vue3-cookies"
export default {
    data() {
        return {
          screening_id: this.$route.query.id,
          quantity: 0,
          screening: null,
          user: null,
          venue: null,
          show: null,
          edit: false,
          ticket: null,
          loaded: false,
          qr_url: null,
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
      await this.GetVenue()
      await this.GetShow()
      await this.GetTicket()

      this.loaded = true
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
      },
      async GetTicket(){
        let screening_id = this.screening_id
        let user_id = this.user.id
        let req = {
          "method": "GET",
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ this.jwt
          },
        }
        let res = await fetch(import.meta.env.VITE_APP_BACKEND_URL + `/tickets/get?jwt=${this.jwt}&screening_id=${screening_id}&user_id=${user_id}`, req)
        let data = await res.json()

        if(res.status == 200){
          this.ticket = data
          this.quantity = parseInt(this.ticket.quantity)
          this.qr_url = `data:image/png;base64, ${data.qr_code}`
        }
      },
      async BookTicket(){
        if(this.ticket) this.edit = true
        if(!this.edit){
          let req = {
            "method": "POST",
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer '+ this.jwt
            },
            body: JSON.stringify({
              screening_id: this.screening_id,
              user_id: this.user.id,
              quantity: this.quantity
            })
          }
          let res = await fetch(import.meta.env.VITE_APP_BACKEND_URL + `/tickets/`, req)
          let data = await res.json()

          this.$toast.show(res.status, data.message)

          await this.GetScreening()
          await this.GetTicket()
        }
        else{
          let req = {
            "method": "POST",
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer '+ this.jwt
            },
            body: JSON.stringify({
              id: this.ticket.id,
              screening_id: this.screening_id,
              user_id: this.user.id,
              quantity: this.quantity
            })
          }
          let res = await fetch(import.meta.env.VITE_APP_BACKEND_URL + `/tickets/edit`, req)
          let data = await res.json()
          this.$toast.show(res.status, data.message)
          if(res.status == 200){
            await this.GetScreening()
            await this.GetTicket()
          }
        }
      }
    },
    computed: {
      price(){
        return this.screening.price * this.quantity
      }
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
            if(this.quantity > 0)
              this.quantity -= 1
          }">-</div>
          <input class="ticket-count" type="text" v-model="quantity" disabled>
          <div class="button increment" @click="()=>{
            if(this.quantity < screening.available)
              this.quantity += 1
          }">+</div>
          <div class="cost">₹ {{ this.price }}</div>
          <div class="book" @click="BookTicket">Book!</div>
        </div>
      </div>
      <div class="split ticket-column">
        <div class="ticket" v-if="ticket">
          <div class="title"><div class="bold">{{ show.name }}</div> @   <div class="bold">{{ venue.name }}</div></div>
          <div class="confirmation">Your ticket is CONFIRMED!</div>

          <img class="qr" v-if="qr_url" :src="this.qr_url">
          <div class="alt" v-else>Qr-loading</div>

          <div class="venue">{{ venue.location }}</div>

          <div class="booked">{{ ticket.quantity }} tickets</div>
        </div>
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
.cost{
  color: #FEFEDF;
  font-size: 28px;
  font-weight: 800;
  margin: auto;
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
.ticket{
  width: 90%;
  height: 90%;
  border-radius: 10px;
  background-color: #845EC2;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.ticket .title{
  width: 100%;
  text-align: center;
  color: #FEFEDF;
  margin-top: 30px;
}
.ticket .bold{
  display: inline-block;
  font-size: 24px;
  font-weight: 800;
  color: #F9F871;
}
.ticket .confirmation{
  margin-top: 10px;
  color: #FEFEDF;
}
.ticket .venue{
  margin-top: 50px;
  color: #FEFEDF;
}
.ticket .booked{
  margin-top: auto;
  margin-bottom: 40px;
  font-size: 46px;
  font-weight: 800;
  color: #D5CABD;
}
.qr{
  width: 200px;
  height: 200px;
  margin-top: 50px;
}
</style>
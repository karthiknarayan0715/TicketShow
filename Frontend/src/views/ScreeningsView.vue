<script>
import ScreeningsBox from '../components/ScreeningsBox.vue';
import {useCookies} from "vue3-cookies"
export default {
    data() {
        return {
          all_shows: [],
          screenings_array: [],
          show_id: "",
          venue: {},
          screenings: {},
          venue_id: this.$route.query.venue_id,
          show_name: "",
          search_query: "",
          date_time: "",
          price: "",
          admin: false,
          edit: false,
          OverlayOpen: false,
        }
    },
    async mounted(){
      if(!this.$login.verify()){
        this.$router.push("/login")
        this.$toast.show("400", "Not logged in or session expired")
      }
      this.jwt = this.$login.verify()
      this.GetVenueData()
      this.user = await this.$login.getUserData();
      this.admin = this.user.role == "admin"
      this.GetShows()
      await this.GetScreenings()
    },
    methods: {
      async GetVenueData(){
        let req = {
            "method": "GET",
            headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ this.jwt
          }
          }
          const res = await fetch(import.meta.env.VITE_APP_BACKEND_URL + `/venues/get?id=${this.venue_id}&jwt=${this.jwt}`, req)
          const data = await res.json()
          if(res.status == 200){
            this.venue = data
          }
      },
      async GetShows(){
          let req = {
            "method": "GET",
            headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ this.jwt
          }
          }
          const res = await fetch(import.meta.env.VITE_APP_BACKEND_URL + `/shows/get?jwt=${this.jwt}`, req)
          const data = await res.json()
          if(res.status == 200){
            this.all_shows = data
          }
        },
      async GetScreenings(){
        let req = {
          "method": "GET",
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ this.jwt
          },
        }
        let res = await fetch(import.meta.env.VITE_APP_BACKEND_URL + `/screenings/get?jwt=${this.jwt}`, req)
        let data = await res.json()

        this.screenings_array = data

        this.SortScreenings()
      },
      async SortScreenings(){
        this.screenings = {}
        this.screenings_array.forEach(screening =>{
          let show = this.all_shows.filter((show)=>{
            return show.id == screening.show_id
          })[0]
          if(Object.keys(this.screenings).includes(show.name)){
            if(Object.keys(this.screenings[show['name']]).includes(screening.date))
              this.screenings[show['name']][screening.date].push(screening)
            else
            this.screenings[show['name']][screening.date] = [screening]
          }
          else{
            this.screenings[show['name']] = {}
            this.screenings[show['name']][screening.date] = [screening]
          }
        })
        console.log(this.screenings)
      },
      async AddScreening(){
        let datetime = new Date(this.date_time)
        let date = `${datetime.getDate()}/${datetime.getMonth()+1}/${datetime.getFullYear()}`
        let time = `${datetime.toLocaleString([], {
          hour: '2-digit',
          minute: '2-digit'
        })}`
        let req = {
            "method": "POST",
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer '+ this.jwt
            },
            body: JSON.stringify({
              venue_id: this.venue_id,
              show_id: this.show_id,
              date: date,
              time: time,
              price: this.price
            })
          }
        let res = await fetch(`${import.meta.env.VITE_APP_BACKEND_URL}/screenings/`, req)
        let data = await res.json()
        this.$toast.show(res.status, data.message)
        if(res.status == 200)
          this.GetScreenings()
      },
      async EditScreening(id){
        let datetime = new Date(this.date_time)
        let date = `${datetime.getDate()}/${datetime.getMonth()+1}/${datetime.getFullYear()}`
        let time = `${datetime.toLocaleString([], {
          hour: '2-digit',
          minute: '2-digit'
        })}`
        let req = {
            "method": "POST",
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer '+ this.jwt
            },
            body: JSON.stringify({
              id: this.id,
              venue_id: this.venue_id,
              show_id: this.show_id,
              date: date,
              time: time,
              price: this.price
            })
          }
        let res = await fetch(`${import.meta.env.VITE_APP_BACKEND_URL}/screenings/edit`, req)
        let data = await res.json()
        this.$toast.show(res.status, data.message)
        if(res.status == 200){
          this.GetScreenings()
          this.OverlayOpen = false
        }
      },
      async DeleteScreening(id){
        let req = {
            "method": "DELETE",
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer '+ this.jwt
            },
          }
        let res = await fetch(`${import.meta.env.VITE_APP_BACKEND_URL}/screenings/delete?id=${id}`, req)
        let data = await res.json()
        this.$toast.show(res.status, data.message)
        if(res.status == 200){
          this.GetScreenings()
        }
      },
      OpenAddScreeningWindow(show_id, venue_id, show_name, date_time, price, edit = false, id=null) {
        this.show_id = show_id;
        this.venue_id = venue_id;
        this.show_name = show_name;
        this.date_time = date_time;
        this.price = price;
        this.edit = edit
        if(this.edit && this.id!=null) console.error("Id  not provided")
        this.id = id
        this.OverlayOpen = true
        // console.log(this.suggestions)
      }
    },
    computed: {
      suggestions(){
        return this.all_shows.filter((show)=>{
          return show.name.includes(this.search_query)
        })
      }
    },
    components: { ScreeningsBox }
};
</script>

<template>
  <main>
    <div class="main">
      <div class="screenings" :class="{admin:admin}">
        <div class="screening">
          <ScreeningsBox :show_name="show_name" :screenings="screenings[show_name]" v-for="show_name in Object.keys(screenings)" @edit="(id)=>{
            let screening = screenings_array.filter((s)=>{
              return s.id == id
            })[0]
            let show = all_shows.filter((show)=>{
              return show.id === screening.show_id
            })[0]
            OpenAddScreeningWindow(screening.show_id, screening.venue_id, show.name, screening.time, screening.price, true, screening.id)
          }" @delete="(id)=>{
            let screening = screenings_array.filter((s)=>{
              return s.id == id
            })[0]
            DeleteScreening(screening.id) 
          }" :is_admin="admin" />
        </div>
      </div>
      <div class="container" v-if="admin"><div class="add-screening" @click="()=>{
        OpenAddScreeningWindow(this.show_id, this.venue_id, this.time, this.price)
      }">Add Screening</div></div>
    </div>
    <div class="overlay" v-if="OverlayOpen ">
      <div class="box">
        <div class="header">
          <div class="name-field"><div class="name">{{ this.user.username }} | {{ this.venue.name }}</div></div>
          <div class="close" @click="()=>this.OverlayOpen = false">X</div>
        </div>
        <div class="form">
          <div class="fields">
            <div class="field"><input type="text" placeholder="Venue ID" v-model="this.venue_id" disabled></div>
            <div class="field"><input type="text" placeholder="Show ID" v-model="this.show_id" disabled></div>
            <div class="field"><input type="text" placeholder="Show Name" v-model="this.show_name" disabled></div>
            <div class="field"><input type="datetime-local" placeholder="Time" v-model="this.date_time"></div>
            <div class="field"><input type="numerical" placeholder="Price" v-model="this.price"></div>
            <div class="button" @click="()=>AddScreening()" v-if="!edit">Add Screening</div>
            <div class="button" @click="()=>EditScreening()" v-else>Edit Screening</div>
          </div>
          <div class="suggestions">
            <div class="title">Select the show</div>
            <div class="box">
              <div class="search"><input type="text" placeholder="Search" v-model="search_query"></div>
              <div class="suggestion" :class="{selected: show.id == this.show_id}" @click="()=>{
                this.show_id = show.id;
                this.show_name = show.name;
              }" v-for="show in this.suggestions">
                {{show.name}}
              </div>              
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.main{
  width: 100%;
  height: 100%;
}
.form{
  width: 100%;
  height: calc(100% - 40px);
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(214, 93, 177, 0.6);
  border-radius: 5px;
}
.fields{
  width: 50%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  margin: 20px;
}
.field{
  width: calc(100%-20px);
  display: flex;
  justify-content: center;
  margin: 10px;
}
input{
  width: 300px;
  height: 30px;
  text-align: center;
  border-radius: 5px;
}
.button{
  width: 130px;
  height: 40px;
  border-radius: 40px;
  background-color: #2189A7;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}
.button:hover{
  opacity: 0.9;
}
.screenings{
  width: 100%;
  height: 100%;
  display: flex;
}
.screening{
  margin: 20px;
}
.screenings.admin{
  width: 100%;
  height: calc(100% - 100px);
}
.add-screening{
  width: 80%;
  height: 50px;
  background-color: #008E9B;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50px;
  cursor: pointer;
}
.add-screening:hover{
  background-color: #1a919c;
}
.container{
  width: 100%;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.overlay{
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.6);
}
.overlay .box{
  width: 70%;
  height: 450px;
}
.overlay .box .header{
  width: 100%;
  height: 40px;
  display: flex;
  justify-content: right;
  background-color: rgba(26, 26, 26, 0.6);
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
  overflow: hidden;
}
.overlay .box .header .close{
  height: 100%;
  aspect-ratio: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: red;
}
.close{
  cursor: pointer;
}
.close:hover{
  opacity: 0.9;
}
.name-field{
  width: 100%;
  display: flex;
  align-items: center;
}
.name{
  margin-left: 10px;
  color: white;
}
.suggestions{
  width: 50%;
  height: 100%;
  display: flex;
  align-items: center;
  flex-direction: column;
  padding: 20px;
}
.suggestions .title{
  font-size: 20px;
  font-weight: bolder;
  margin-bottom: auto;
  margin-top: 20px;
  color: white;
}
.suggestions .box{
  width: 100%; 
  height: 100%;
  background-color: rgba(26, 26, 26, 0.6);
  margin: 40px;
}
.suggestion{
  width: 100%;
  height: 60px;
  background-color: rgba(26, 26, 26, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  cursor: pointer;
}
.suggestion.selected{
  background-color: rgba(71, 67, 67, 0.6);
  pointer-events: none;
}
.suggestion:hover{
  background-color: rgba(26, 26, 26, 0.6);
}
.search{
  display: flex;
  justify-content: center;
  align-items: center;
}
.search input{
  width: 80%;
  height: 30px;
  margin: 15px;
}
</style>
<script>
import VenueBox from '../components/VenueBox.vue';
import {useCookies} from "vue3-cookies"
export default {
    data() {
        return {
            name: "",
            place: "",
            location: "",
            capacity: "",
            id: -100,
            edit: false,
            user: null,
            admin: false,
            venues: [],
            addVenueBox: false,
        };
    },
    async mounted(){
      if(!this.$login.verify()){
        this.$router.push("/login")
        this.$toast.show("400", "Not logged in or session expired")
      }
      this.jwt = this.$login.verify()
      this.user = await this.$login.getUserData();
      this.admin = this.user.role == "admin"
      this.GetVenues()
    },
    methods: {
        async AddVenue(){
          let req = {
            "method": "POST",
            headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ this.jwt
          },
            body: JSON.stringify({
              name: this.name,
              place: this.place,
              location: this.location,
              capacity: this.capacity,
            })
          }
          const res = await fetch(import.meta.env.VITE_APP_BACKEND_URL + '/venues', req)
          const data = await res.json()
          this.$toast.show(res.status, data.message)
          if(res.status == 200){
            this.addVenueBox = false
            this.GetVenues()
          }
        },
        async EditVenue(){
          let req = {
            "method": "POST",
            headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ this.jwt
          },
            body: JSON.stringify({
              id: this.id,
              name: this.name,
              place: this.place,
              location: this.location,
              capacity: this.capacity,
            })
          }
          const res = await fetch(import.meta.env.VITE_APP_BACKEND_URL + '/venues/edit', req)
          const data = await res.json()
          this.$toast.show(res.status, data.message)
          if(res.status == 200){
            this.addVenueBox = false
            this.GetVenues()
          }
        },
        async GetVenues(){
          const { cookies } = useCookies()
          let req = {
            "method": "GET",
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer '+ this.jwt
            }
          }
          const res = await fetch(import.meta.env.VITE_APP_BACKEND_URL + `/venues/get?jwt=${cookies.get("jwt")}`, req)
          const data = await res.json()
          this.venues = data
          console.log(data)
        },
        async DeleteVenue(id){
          const { cookies } = useCookies();
          const req = {
              method: "DELETE",
              headers: {
                  "Content-Type": "application/json",
                  "Authorization": "Bearer " + cookies.get("jwt")
              }
          }
          const res = await fetch(`${import.meta.env.VITE_APP_BACKEND_URL}/venues/delete?id=${id}`, req); 
          const data = await res.json();

          this.$toast.show(res.status, data.message)
          if(res.status == 200)
          {
              this.GetVenues()
          }
      },
      async GetVenueData(id){
        const {cookies} = useCookies();
        let req = {
              "method": "GET",
              headers: {
                  'Content-Type': 'application/json',
                  'Authorization': 'Bearer '+ this.jwt
              }
            }
            const res = await fetch(`${import.meta.env.VITE_APP_BACKEND_URL}/venues/get?id=${id}&jwt=${cookies.get("jwt")}`, req)
            const data = await res.json()
            return data
      },
      OpenAddVenue(id, name, place, location, capacity, edit = false){
        this.id = id
        this.name = name
        this.place = place
        this.location = location
        this.capacity = capacity
        this.addVenueBox = true
        this.edit = edit
      }
    },
    components: { VenueBox }
};
</script>

<template>
  <main>
    <div class="main">
      <div class="venues" :class="{admin: admin}">
        <div class="venue" v-for="venue in this.venues">
          <VenueBox :is_admin=this.admin :id=venue.id :name=venue.name :place=venue.place :location=venue.location :capacity=venue.capacity @delete="this.DeleteVenue(venue.id)" @edit="this.OpenAddVenue(venue.id, venue.name, venue.place, venue.location, venue.capacity, true)" />
        </div>
      </div>
      <div class="container" v-if="admin"><div class="add-venue" @click="()=>{
        this.OpenAddVenue()
      }">Add Venue</div></div>
    </div>
    <div class="overlay" v-if="addVenueBox ">
      <div class="box">
        <div class="header">
          <div class="name-field"><div class="name">{{ this.user.username }}</div></div>
          <div class="close" @click="()=>this.addVenueBox = false">X</div>
        </div>
        <div class="form">
          <div class="fields">
            <div class="field" v-if="this.edit"><input type="text" placeholder="Name" v-model="this.id" disabled></div>
            <div class="field"><input type="text" placeholder="Name" v-model="this.name"></div>
            <div class="field"><input type="text" placeholder="Place" v-model="this.place"></div>
            <div class="field"><input type="text" placeholder="Location" v-model="this.location"></div>
            <div class="field"><input type="text" placeholder="Capacity" v-model="this.capacity"></div>
            <div class="button" @click="()=>AddVenue()" v-if="!edit">Add Venue</div>
            <div class="button" @click="()=>EditVenue()" v-else>Edit Venue</div>
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
  width: 500px;
  height: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(214, 93, 177, 0.2);
  border-radius: 5px;
}
.fields{
  display: flex;
  align-items: center;
  flex-direction: column;
  margin: 20px;
}
.field{
  width: 100%;
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
.venues{
  width: 100%;
  height: 100%;
}
.venues.admin{
  width: 100%;
  height: calc(100% - 100px);
}
.add-venue{
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
.add-venue:hover{
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
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.26);
}
.overlay .box{
  width: 70%;
  height: 50%;
}
.overlay .box .header{
  width: 100%;
  height: 40px;
  display: flex;
  justify-content: right;
  background-color: rgba(26, 26, 26, 0.342);
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
.overlay .box .form {
  width: 100%;
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
.venues{
  display: flex;
}
.venue{
  margin: 20px;
}
</style>
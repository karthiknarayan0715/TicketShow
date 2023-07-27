<script>
import ScreeningsBox from '../components/ScreeningsBox.vue';
import {useCookies} from "vue3-cookies"
export default {
    data() {
        return {
          show_id: "",
          venue_id: "",
          date_time: "",
          price: "",
          admin: false,
          screenings: ['1:30 PM', '2:30 PM', '3:30 PM']
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
        OpenAddScreeningWindow(show_id, venue_id, date_time, price){
          
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
          <ScreeningsBox show_name="SHOW" :screenings="screenings" />
        </div>
      </div>
      <div class="container" v-if="admin"><div class="add-screening" @click="()=>{
        
      }">Add Screening</div></div>
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
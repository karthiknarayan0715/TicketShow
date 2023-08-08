<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useCookies } from 'vue3-cookies';
</script>
<script>
export default {
  data() {
    return {
      user: {},
      dropDown: false,
      isLoggedIn: false,
      query: ""
    }
  },
  mounted(){
    this.isLoggedIn = this.$login.verify()

    this.user = this.$login.getUserData()
    if(!this.user) this.Logout()
  },
  methods: {
    
    ToggleDropDown(){
      this.dropDown = !this.dropDown
    },
    SetLoggedIn(val){
      this.isLoggedIn = val
    },
    Logout() {
      const { cookies } = useCookies()
      this.dropDown = false
      this.isLoggedIn = false
      cookies.remove("jwt")
      this.$router.push("/login")
    }
  }
}
</script>

<template>
  <div id="header">
    <div class="title" @click="()=>this.$router.push('/')">Ticket Show</div>
    <div class="search"><input type="search" placeholder="search?" v-model="this.query" style="height: 40px; width: 300px; margin-left: 30px; padding: 15px;"><div class="submit" @click="this.$router.push(`/search?query=${query}`)">Search</div></div>
    <div class="to-right">
      <div class="nav-button" v-if="!this.isLoggedIn" @click="()=>this.$router.push('/login')">Login</div>
      <div class="nav-button" v-if="!this.isLoggedIn" @click="()=>this.$router.push('/register')">Register</div>
      <div class="profile" @click="this.ToggleDropDown" v-if="this.isLoggedIn"><span class="material-symbols-outlined" v-if="this.$login.verify">
        account_circle
      </span></div>
      <div class="drop-down" :class="{show: dropDown}">
        <div class="drop-down-content" v-if="dropDown">
          <div class="drop-down-item" @click="this.$router.push('/')">Home</div>
          <div class="drop-down-item" @click="()=>{
            this.$router.push(`/venues/`)
            this.ToggleDropDown()
          }">Venues</div>
          <div class="drop-down-item" @click="()=>{
            this.$router.push(`/shows/`)
            this.ToggleDropDown()
          }">Shows</div>
          <div class="drop-down-item" @click="this.Logout">Logout</div>
        </div>
      </div>
    </div>
  </div>
  <RouterView @logged_in="this.SetLoggedIn" />
</template>

<style scoped>
  .profile{
    cursor: pointer;
  }
  #header{
    width: 100%;
    height: 80px;
    background-color: rgba(44, 115, 210, 0.3);
    display: flex;
    align-items: center;
  }
  .title{
    font-size: 32px;
    margin-left: 20px;
    color: white;
    cursor: pointer;
  }
  .search{
    display: flex;
  }
  .search .submit{
    margin-left: 10px;
    width: 100px;
    padding: 10px;
    background-color: #C34A36;
    text-align: center;
    border-radius: 10px;
    color: white;
    cursor: pointer;
  }
  .search .submit:hover{
    background-color: #a84634;
  }
  .to-right{
    margin-left: auto;
    margin-right: 20px;
    display: flex;
  }
  .nav-button{
    width: 100px;
    height: 40px;
    background-color: #C34A36;
    margin-left: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    border-radius: 5px;
    transition-duration: 100ms;
    cursor: pointer;
  }
  .nav-button:hover{
    background-color: #FEFEDF;
    color: black;
  }
  .drop-down{
    position: absolute;
    right: 0;
    top: 80px;
    background-color: #FBEAFF;
    width: 200px;
    height: auto;
    transform-origin: top left;
    transform: scaleY(0);
    overflow: hidden;
    transition-duration: 200ms;
  }
  .drop-down-item{
    width: 100%;
    height: 40px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .drop-down.show{
    transform: scaleY(1);
  }
  .drop-down-item:hover{
    background-color: #dbc3e1;
  }
</style>

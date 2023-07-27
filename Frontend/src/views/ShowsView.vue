<script>
import ShowBox from '../components/ShowBox.vue';
import {useCookies} from "vue3-cookies"
export default {
    data() {
        return {
          name: "",
          description: "",
          duration: "",
          rating: "",
          id: -100,
          edit: false,
          user: null,
          admin: false,
          shows: [],
          addShowBox: false,
        };
    },
    async mounted(){
      if(!this.$login.verify()){
        this.$router.push("/")
        this.$toast.show("200", "Already logged in!")
      }
      this.jwt = this.$login.verify()
      this.user = await this.$login.getUserData();
      this.admin = this.user.role == "admin"
      this.GetShows()
    },
    methods: {
      async AddShow(){
          let req = {
            "method": "POST",
            headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ this.jwt
          },
            body: JSON.stringify({
              name: this.name,
              description: this.description,
              duration: this.duration,
              rating: this.rating,
            })
          }
          const res = await fetch(import.meta.env.VITE_APP_BACKEND_URL + '/shows', req)
          const data = await res.json()
          this.$toast.show(res.status, data.message)
          if(res.status == 200){
            this.addShowBox = false
            this.GetShows()
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
            this.shows = data
          }
        },
        async EditShow(){
          let req = {
            "method": "POST",
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer '+ this.jwt
            },
            body: JSON.stringify({
              id: this.id,
              name: this.name,
              description: this.description,
              duration: this.duration,
              rating: this.rating,
            })
          }
          const res = await fetch(import.meta.env.VITE_APP_BACKEND_URL + '/shows/edit', req)
          const data = await res.json()
          this.$toast.show(res.status, data.message)
          if(res.status == 200){
            this.addShowBox = false
            this.GetShows()
          }
        },
        async DeleteShow(id){
          const { cookies } = useCookies();
          const req = {
              method: "DELETE",
              headers: {
                  "Content-Type": "application/json",
                  "Authorization": "Bearer " + cookies.get("jwt")
              },
          }
          const res = await fetch(`${import.meta.env.VITE_APP_BACKEND_URL}/shows/delete?id=${id}`, req); 
          const data = await res.json();

          this.$toast.show(res.status, data.message)
          if(res.status == 200)
          {
              this.GetShows()
          }
        },
        async GetShowsData(id){
          const {cookies} = useCookies();
          let req = {
                "method": "GET",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer '+ this.jwt
                }
              }
              const res = await fetch(`${import.meta.env.VITE_APP_BACKEND_URL}/shows/get?id=${id}&jwt=${cookies.get("jwt")}`, req)
              const data = await res.json()
              return data
        },
        OpenAddShow(id, name, description, duration, rating, edit = false){
          this.id = id
          this.name = name
          this.description = description
          this.duration = duration
          this.rating = rating
          this.addShowBox = true
          this.edit = edit
        }
    },
    components: { ShowBox }
};
</script>

<template>
  <main>
    <div class="main">
      <div class="shows" :class="{admin: admin}" >
        <div class="show" v-for="show in this.shows">
          <ShowBox :is_admin=this.admin :id=show.id :name=show.name :description=show.desc :duration=show.duration :capacity=show.rating @delete="this.DeleteShow(show.id)" @edit="this.OpenAddShow(show.id, show.name, show.desc, show.duration, show.rating, true)" />
        </div>
      </div>
      <div class="container" v-if="admin"><div class="add-show" @click="()=>{this.OpenAddShow(this.id, this.name, this.description, this.duration, this.rating)}">Add Show</div></div>
    </div>
    <div class="overlay" v-if="addShowBox">
      <div class="box">
        <div class="header">
          <div class="name-field"><div class="name">{{ this.user.username }}</div></div>
          <div class="close" @click="()=>this.addShowBox = false">X</div>
        </div>
        <div class="form">
          <div class="fields">
            <div class="field"><input type="text" placeholder="name" v-model="this.name"></div>
            <div class="field"><input type="text" placeholder="description" v-model="this.description"></div>
            <div class="field"><input type="text" placeholder="duration" v-model="this.duration"></div>
            <div class="field"><input type="text" placeholder="rating" v-model="this.rating"></div>
            <div class="button" @click="()=>AddShow()" v-if="!edit">Add show</div>
            <div class="button" @click="()=>EditShow()" v-else>Edit show</div>
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
.shows{
  width: 100%;
  height: 100%;
}
.shows.admin{
  width: 100%;
  height: calc(100% - 100px);
}
.add-show{
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
.add-show:hover{
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
.shows{
  display: flex;
}
.show{
  margin: 20px;
}
</style>
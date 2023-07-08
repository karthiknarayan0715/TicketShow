<script>
import ToastMessage from '../components/ToastMessage.vue';
import { useCookies } from 'vue3-cookies';
export default {
    data() {
        return {
            username: "",
            password: ""
        };
    },
    mounted(){
      if(this.$login.verify()){
        this.$router.push("/")
        this.$toast.show("200", "Already logged in!")
      }
    },
    methods: {
        setUsername(val) {
            this.username = val;
        },
        setPassword(val) {
            this.password = val;
        },
        async Login() {
          const { cookies } = useCookies()
            let req = {
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": JSON.stringify({
                    "username": this.username,
                    "password": this.password
                })
            };
            const res = await fetch(`${import.meta.env.VITE_APP_BACKEND_URL}/users/login`, req);
            const data = await res.json();
            if(data.status == 200){
              this.$emit('logged_in', true)
              cookies.set("jwt", data.jwt)
              this.$router.push("/")
            }
            this.$toast.show(data.status, data.message)
        }
    },
    components: { ToastMessage }
};
</script>

<template>
  <main>
    <div class="main">
      <div class="form">
        <div>
          <div class="field"><input type="text" placeholder="username" v-model="username"></div>
          <div class="field"><input type="password" placeholder="password" v-model="password"></div>
          <div class="field"><div class="button" @click="Login">Login</div></div>
        </div>
      </div>
    </div>
  </main>
</template>

<style>
.main{
  display: flex;
  width: 100%;
  height: 100%;
  justify-content: center;
  align-items: center;
}
.form{
  width: 500px;
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(214, 93, 177, 0.2);
  border-radius: 5px;
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
  width: 100px;
  height: 40px;
  background-color: #FF9671;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}
.button:hover{
  opacity: 0.9;
}
</style>
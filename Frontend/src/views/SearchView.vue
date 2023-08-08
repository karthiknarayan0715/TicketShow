<script>
import ToastMessage from '../components/ToastMessage.vue';
import { useCookies } from 'vue3-cookies';
export default {
    data() {
        return {
            query: this.$route.query.query,
            loading: true,
            results: null
        };
    },
    async mounted(){
      if(!this.query) this.$router.push("/")
      await this.GetResults()
    },
    methods: {
        async GetResults(){
          this.loading = true
          let res = await fetch(`${import.meta.env.VITE_APP_BACKEND_URL}/search?query=${this.query}`)
          let data = await res.json()
          this.results = data
          console.log(data)
          this.loading = false
        }
    },
    components: {  }
};
</script>

<template>
  <main>
    <div class="main" v-if="!loading">
      <div class="title"  v-if="this.results['venues'].length > 0">Venues</div>
      <div class="venues">
          <div class="tag" v-for="venue in this.results['venues']" @click="this.$router.push('/screenings?venue_id='+venue.id)">{{venue.name}}</div>
      </div>
      <div class="title" style="margin-top: 30px;"  v-if="this.results['shows'].length > 0">Shows</div>
      <div class="shows">
        <div class="tag" v-for="show in this.results['shows']" @click="this.$router.push('/screenings?show_id='+show.id)">{{show.name}}</div>
      </div>
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
}
.title{
  font-size: 24px;
  font-weight: 800;
}
.venues{
  margin-top: 20px;
  display: flex;
}
.shows{
  margin-top: 20px;
  display: flex;
}
.tag{
  padding: 10px;
  border-radius: 10px;
  border: 1px solid black;
  cursor: pointer;
  margin-left: 5px;
  margin-right: 5px;
}
.tag:hover{
  border: 1px solid rgba(37, 34, 34, 0.699);
}
</style>
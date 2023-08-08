<script>
import { useCookies } from 'vue3-cookies';

export default {
  data(){
    return{
      text: "WELCOME TO TICKET SHOW",
      index: 0,
      changing: false,
      messages: [
        "WELCOME TO TICKET SHOW",
        "Step Right Up! Experience the Ticket Show Extravaganza!",
        "Tickets Unleashed! Prepare for an Unforgettable Showtime!",
        "Unlock the Magic: Your Ticket to a Mesmerizing Show!",
        "Roll the Dice, Grab a Ticket, Let the Show Begin!",
        "Tickets of Wonder: Your Gateway to a Spectacular Showcase!"
      ]
    }
  },
  methods: {
    Animate(){
      setInterval(()=>{
        if(this.index >= this.messages.length-1) this.index = 0
        else this.index = this.index + 1
        this.changing = true
        setTimeout(()=>{
          this.changing = false
          this.text = this.messages[this.index]
        }, 1000)
      }, 4000)
    }
  },
  mounted() {
    this.Animate()
  }
}
</script>

<template>
  <main>
    <div class="main">
      <div class="welcome" :class="{changing: this.changing}">{{text}}</div>
    </div>
  </main>
</template>
  
  <style scoped>
  .main{
    width: 100%;
    height: 100%;
  }
  .welcome{
    width: 100%;
    height: 100%;
    font-size: 48px;
    font-weight: 800;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    opacity: 1;
    transition: opacity 500ms;
    color: #FFC75F;
  }
  .welcome.changing{
    opacity: 0;
  }
  </style>
  
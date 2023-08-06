<script>
    export default {
        props: ['id', 'name', 'place', 'location', 'capacity', 'is_admin'],
        mounted(){
            console.log(this.is_admin)
            if(this.is_admin === true)
            {
                this.admin = true;
            }
        },
        data() {
            return {
                admin: false,
            }
        },
        methods: {
            
        }
    }
</script>

<template>
    <div class="box">
        <div class="title">
            <div class="name" @click="this.$router.push(`/screenings?venue_id=${this.id}`)">{{ name }}</div>
            <div class="id">{{ id }}</div>
        </div>
        <div class="address" :class="{admin: admin}">
            <div>
            <div class="place">{{ place }}</div>
            <div class="location">{{ location }}</div>
            </div>
        </div>
        <div class="footer" v-if="this.admin">
            <div class="box-button" v-if="this.admin" @click="()=>this.$emit('edit')">Edit</div>
            <div class="box-button red" v-if="this.admin" @click="()=>this.$emit('delete')">Delete</div>
        </div>
    </div>
</template>

<style scoped>
.box{
    width: 250px;
    height: 200px;
    border-radius: 10px;
    background-color: #845EC2;
}
.title{
    background-color: #724faa;
    width: calc(100% - 20px);
    height: 40px;
    padding: 10px;
    text-align: center;
    color: white;
    font-weight: bolder;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}
.name{
    font-size: 24px;
    cursor: pointer;
}
.id{
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgb(158, 158, 158);
    font-size: 10px;
    font-weight: bolder;
}
.address{
    width: 100%;
    height: calc(100% - 60px);
    display: flex;
    justify-content: center;
    align-items: center;
}
.address.admin{
    height: calc(100% - 115px);
}
.place{
    width: 100%;
    text-align: center;
    color: rgb(66, 66, 66);
}
.location{
    width: 100%;
    text-align: center;
    color: rgb(66, 66, 66);
    font-size: 12px;
}
.footer{
    width: 100%;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.box-button{
    height: 30px;
    padding: 5px;
    width: 80px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 30px;
    cursor: pointer;
    margin: auto;
    background-color: #00C9A7;
}
.box-button:hover {
    opacity: 0.9;
}
.box-button.red{
    background-color: #C34A36;
    color: white;
}
</style>
<script>
    export default {
        props: ['id', 'name', 'duration', 'description', 'rating', 'is_admin'],
        mounted(){
            if(this.is_admin === true)
            {
                this.admin = true;
            }
        },
        data() {
            return {
                admin: false
            }
        },
        methods: {
            
        }
    }
</script>

<template>
    <div class="box">
        <div class="title">
            <div class="name">{{ name }}</div>
            <div class="id">{{ id }}</div>
        </div>
        <div class="duration">{{ duration }}</div>
        <div class="rating">{{ rating }}</div>
        <div class="description"><div class="text">{{ description.length > 100 ? description.substr(0, 100) + "..." : description }}</div></div>
        <div class="footer">
            <div class="box-button" v-if="this.admin" @click="this.$emit('edit')">Edit</div>
            <div class="box-button red" v-if="admin" @click="this.$emit('delete')">Delete</div>
        </div>
    </div>
</template>

<style scoped>
.box{
    width: 250px;
    height: 160px;
    padding: 10px;
    border-radius: 10px;
    background-color: #845EC2;
}
.title{
    width: 100%;
    height: 40px;
    text-align: center;
    color: white;
    font-weight: bolder;
}
.name{
    font-size: 24px;
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
.cast{

    width: 100%;
    height: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-size: 12px;
}
.description{
    width: 100%;
    height: calc(100% - 100px);
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 12px;
    color: rgb(225, 212, 212);
}
.text{
    width: 100%;
    text-align: center;
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
.duration{
    width: 100%;
    height: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-size: 12px;
}
</style>
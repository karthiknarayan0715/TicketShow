<script>
    export default {
        props: ['show_name', 'screenings'],
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
            <div class="name">{{ show_name }}</div>
        </div>
        <div class="screenings">
            <div class="time" v-for="screening in screenings">{{ screening }}</div>
        </div>
    </div>
</template>

<style scoped>
.box{
    width: 100%;
}
.title{
    width: 100%;
    height: 40px;
    color: black;
    font-weight: bolder;
}
.name{
    font-size: 24px;
}
.screenings{
    width: 100%;
    display: flex;
}
.time{
    padding: 15px;
    margin: 10px;
    font-weight: 700;
    border: 1px solid #00C9A7;
    color: #00C9A7;
    cursor: pointer;
}
.time:hover{
    box-shadow: 2px 2px;
}
</style>
<script>
    export default {
        props: ['show_name', 'screenings', 'is_admin'],
        mounted(){
            if(this.is_admin === true)
            {
                this.admin = true;
            }
        },
        data() {
            return {
                admin: false,
                edit_opened_screening_id: null,
            }
        },
        methods: {
            HandleRightClick(e, id){
                e.preventDefault();
                if(this.edit_opened_screening_id === id) 
                    this.edit_opened_screening_id = null;
                else
                    this.edit_opened_screening_id = id
            },
        }
    }
</script>

<template>
    <div class="box">
        <div class="title">
            <div class="name">{{ show_name   }}</div>
        </div>
        <div class="screenings">
            <div class="screening-date" v-for="date in Object.keys(screenings)">
                <div class="date">{{ date }}</div>
                <div class="show-times">
                <div class="time-container" v-for="screening in screenings[date]">
                    <div class="time" @click="this.$router.push(`/screenings/book?id=${screening.id}`)" v-on:click.right="(e)=>{
                        if(admin)
                            HandleRightClick(e, screening.id)
                    }">{{ screening.time }}</div>
                    <div class="right-click-dropdown" :class="{selected: this.edit_opened_screening_id === screening.id}" v-if="admin">
                        <div class="dropdown-item" @click="()=>{
                            this.edit_opened_screening_id = null
                            this.$emit('edit', screening.id)
                        }">Edit</div>
                        <div class="dropdown-item" @click="this.$emit('delete', screening.id)">Delete</div>
                    </div>
                </div>
                </div>
            </div>
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
}
.screening-date{
    margin-left: 40px;
}
.date{
    font-weight: bolder;
}
.show-times{
    margin-left: 20px;
    display: flex;
}
.time{
    max-width: 80px;
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
.right-click-dropdown{
    position: absolute;
    width: 100px;
    height: auto;
    margin-left: 10px;
    font-weight: 700;
    background-color: red;
    transform-origin: top left;
    transform: scaleY(0);
    overflow: hidden;
    transition-duration: 200ms;
}
.right-click-dropdown.selected{
    transform: scaleY(1);
}
.dropdown-item{
    width: 100%;
    padding: 15px;
    background-color: antiquewhite;
    cursor: pointer;
}
.dropdown-item:hover{
    background-color: rgb(237, 221, 199);
}
</style>
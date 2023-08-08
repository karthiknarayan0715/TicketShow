<script>
    export default {
        props: ['screening', 'is_admin'],
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
                    <div class="time" @click="this.$router.push(`/screenings/book?id=${screening.id}`)" v-on:click.right="(e)=>{
                        if(admin)
                            this.$emit('rightclick', e)
                    }">{{ screening.time }}</div>
                    
                </div>
</template>

<style scoped>
.time{
    max-width: 100px;
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
<script>
    export default {
        data() {
            return {
                visible: false,
                status: "",
                message: ""
            };
        },
        methods: {
            show(){
                this.visible = true
                setTimeout(()=>{
                    this.visible = false
                }, 3000)
            }
        }
    }
</script>

<template>
    <div class="toast-message" :class="{show: visible}">
        <div class="header" v-if="parseInt(status / 100) === 2" style="background-color: rgb(69, 186, 69);">
            <div class="title">MESSAGE</div>
            <div class="status-code">{{ status }}</div>
        </div>
        <div class="header" v-else style="background-color: red; color: white;">
            <div class="title">MESSAGE</div>
            <div class="status-code">{{ status }}</div>
        </div>
        <div class="message">{{ message }}</div>
    </div>
</template>

<style scoped>
    .toast-message{
        position: absolute;
        bottom: 10px;
        right: 10px;
        width: 300px;
        height: 100px;
        border-radius: 5px;
        background-color: antiquewhite;
        opacity: 0;
        transition-duration: 200ms;
    }
    .toast-message.show{
        opacity: 1;
    }
    .header{
        width: 100%;
        height: 30px;
        display: flex;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        align-items: center;
    }
    .title{
        margin-left: 10px;
    }
    .status-code{
        margin-left: auto;
        margin-right: 10px;
    }
    .message{
        width: 100%;
        height: calc(100% - 30px);
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>
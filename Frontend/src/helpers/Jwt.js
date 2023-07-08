import { useCookies } from "vue3-cookies"

const cookies = useCookies()

const set = (token)=>{
    cookies.set("jwt", token)
}

const verifyJWT = async ()=>{
    let jwt = cookies.get("jwt")

    let headers = {
        "method": "POST",
        "Authorization": `Bearer ${jwt}`
    }

    let res = await fetch(`${process.env.VUE_APP_BACKEND_URL}/users/verify`)

}
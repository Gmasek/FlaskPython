import {Navigate} from "react-router-dom"
import {jwtDecode} from "jwt-decode"
import api from "../api"
import { useState ,useEffect} from "react"

function ProtectedRoute({children}){
    const [isAuthorized, setIsAuthorized] = useState(null)

    useEffect(() =>{∂
        auth().catch(()=>setIsAuthorized(false))
    },[])

    const refreshToken = async () =>{
        const refreshToken = localStorage.getItem("REFRESH_TOKEN")
        try{
            const res = await api.post(
                "/refresh",
                {refresh: refreshToken}
            )
            if (res.status ==  200){
                localStorage.setItem("ACCESS_TOKEN",res.data.access)
                console.log("jó")
                setIsAuthorized(true)
            }
            else {
                setIsAuthorized(false)
            }
        }
        catch(err){
            console.log(err)
            setIsAuthorized(false)
        }
    } 
    const auth = async () => {
        const token = localStorage.getItem("ACCESS_TOKEN")
        if (!token){
            setIsAuthorized(false)
            return;
        }
        const decoded = jwtDecode(token)
        const token_expire = decoded.exp
        const now  = Date.now()/1000

        if (token_expire < now){
            await refreshToken()
        }
        else{
            setIsAuthorized(true)
        }
    }
    if (isAuthorized ==null){
        return <div>Loading..</div>
    }

    return isAuthorized ? children : <Navigate to="/login" />
}

export default ProtectedRoute;
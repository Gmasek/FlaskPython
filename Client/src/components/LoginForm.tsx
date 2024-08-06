import React from 'react'
import api from '../api';
import {  Navigate, useNavigate } from 'react-router-dom';

export default function LoginForm() {
    const navigate = useNavigate();
    interface User {
        email: string;
        password: string;
    }
    const [user, setUser] = React.useState<User>({email: "", password: ""});
    
    async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault();
        try{
            const res = await api.post('/login', {email: user.email , password:user.password});
            console.log(res);
            localStorage.setItem("ACCESS_TOKEN", res.data.access_token);
            localStorage.setItem('REFRESH_TOKEN', res.data.REFRESH_TOKEN);
            console.log(res);
            navigate("/");
        } catch (error) {
            console.log(error);
        }
        

    }  
    async function getUser (event: any) {
        console.log("asd")
        try{
            const res = await api.get('/getuser');
            console.log(res);
        } catch (error) {
            console.log(error);
        }
       
    }

  return (
    <>
    <div className='flex justify-center items-center'>
     <form onSubmit={handleSubmit} className='flex flex-col bg-slate-400 w-2/5 '>
        <label htmlFor="email">Email</label>
        <input type="email" name="email" id="email"  onChange={(e) => setUser({...user, email: e.target.value})}/>
        <label htmlFor="password">Password</label>
        <input type="password" name="password" id="password" onChange={(e) => setUser({...user, password: e.target.value}  
        )}/>
        <button type="submit">Login</button>
    </form>
       
    </div>
         <button onClick={() =>navigate("/register")}>Register</button>
         </>
  )
}
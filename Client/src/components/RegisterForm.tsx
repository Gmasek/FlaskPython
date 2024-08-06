import React from 'react'
import api from '../api';


export default function RegisterForm({}: Props) {
  interface RegiserUser{
    email: string;
    password: string;
    password2: string;
  }

  const [RegiserUser, setUser] = React.useState<RegiserUser>({email: "", password: "", password2: ""});
  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (RegiserUser.password === RegiserUser.password2) {
      try{
        const res = await api.post('/signup', {email: RegiserUser.email , password:RegiserUser.password});
        console.log(res);
        localStorage.setItem("ACCESS_TOKEN", res.data.access_token);
        localStorage.setItem('REFRESH_TOKEN', res.data.REFRESH_TOKEN);
        console.log(res);
      } catch (error) {
        console.log(error);
      }
    }
    else {
      alert("Passwords don't match")
    }
  }

  return (
    <div className='flex justify-center items-center'>
     <form onSubmit={handleSubmit} className='flex flex-col bg-slate-400 w-2/5 '>
        <label htmlFor="email">Email</label>
        <input type="email" name="email" id="email"  onChange={(e) => setUser({...RegiserUser, email: e.target.value})}/>
        <label htmlFor="password">Password</label>
        <input type="password" name="password" id="password" onChange={(e) => setUser({...RegiserUser, password: e.target.value}  
        )}/>
         <label htmlFor="password">Password again</label>
        <input type="password" name="password" id="password" onChange={(e) => setUser({...RegiserUser, password2: e.target.value}  
        )}/>
        <button type="submit">Register</button>
    </form>
    </div>
  )
}


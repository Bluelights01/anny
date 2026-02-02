import { useState } from "react";
import { type FormEvent, useRef } from "react";
import axios from 'axios';
import "./login.css";

export default function LoginWindow({ setLoggedIn ,setusername}:
  {
  setLoggedIn: React.Dispatch<React.SetStateAction<boolean>>;
  setusername: React.Dispatch<React.SetStateAction<string>>
}
) {
  const [newUser, setNewUser] = useState(false);
  const usernameRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);
  const confirmPasswordRef = useRef<HTMLInputElement>(null);
  
        const handleSubmit = async (e: FormEvent) => {
            e.preventDefault();

            if(usernameRef.current==null || passwordRef.current==null){
              alert("values are null")
              return;
            }
            const dataToSend = {
              username: usernameRef.current.value,
              password: passwordRef.current.value
            };

            if (newUser) {
              if(confirmPasswordRef.current==null){
                return;
              }
              const confirmPass = confirmPasswordRef.current.value;
              if (dataToSend.password !== confirmPass) {
                alert("Passwords do not match");
                return;
              }
              const response=await axios.post('http://127.0.0.1:8000/auth/signup',{
                "username": usernameRef.current.value,
                "password": passwordRef.current.value
              });
              if(response.data.status=="success"){
                setNewUser(false);
              }
              else{
                alert("username taken");
              }
              usernameRef.current.value="";
              passwordRef.current.value="";
              confirmPasswordRef.current.value="";
              
            } else {
              console.log("Sending to FastAPI:", dataToSend);
              const response=await axios.post('http://127.0.0.1:8000/auth/login',{
                "username": usernameRef.current.value,
                "password": passwordRef.current.value
              });
              if(response.data.status=="success"){
                alert("succes");
                setLoggedIn(true);
                setusername(usernameRef.current.value);
              }
              else{
                
                usernameRef.current.value="";
                passwordRef.current.value="";
                alert("Invalid creds")
              }
              return;
            }
          };
  return (
   
      <div className="login-box">
        {newUser ? (
          
          <>
            <h2>Create Account</h2>
            <form onSubmit={handleSubmit}>
            <input type="text" placeholder="Username" ref={usernameRef}/>
            <input type="password" placeholder="Password" ref={passwordRef}/>
            <input type="password" placeholder="Confirm Password" ref={confirmPasswordRef}/>
            <button type='submit'>Sign Up</button>
            </form>
            <p>
              Already have an account?{" "}
              <span
                className="toggle-link"
                onClick={() => setNewUser(false)}
              >
                Login
              </span>
            </p>
          </>
        ) : (
         
          <>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
            <input type="text" placeholder="Username" ref={usernameRef}/>
            <input type="password" placeholder="Password" ref={passwordRef}/>
            <button type="submit">Login</button>
            </form>
            <p>
              New user?{" "}
              <span
                className="toggle-link"
                onClick={() => setNewUser(true)}
              >
                Create Account
              </span>
            </p>
          </>
        )}
      </div>
  );
}

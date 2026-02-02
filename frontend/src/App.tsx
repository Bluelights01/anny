import { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import MessageInput from "./components/MessageInput";
import LoginWindow from "./components/login";
import SearchFriend from "./components/SearchFriends";
import Inbox from "./components/inbox"
import bg from "./assets/home.webp";
import "./App.css";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username,setusername] = useState("");
  const [mainwindow,setmainwindow]=useState("home");
  if (!loggedIn) {
    return (
      <div
        className="loginbg"
        style={{ backgroundImage: `url(${bg})` }}
        //onClick={() => setLoggedIn(true)} // example login trigger
      >

         <LoginWindow setusername={setusername} setLoggedIn={setLoggedIn}/>
      </div>
    );
  }

  return (
    <div className="app">
      <Sidebar setmainwindow={setmainwindow} />

      <div className="chat-area">
        {mainwindow === "home" ? (
          <>
            <ChatWindow />
            <MessageInput />
          </>
        ) : mainwindow === "search" ? (
          <SearchFriend username={username}/>
        ) : mainwindow === "inbox" ? (
          <Inbox username={username} />
        ) : null}
      </div>
    </div>
  );
}

export default App;

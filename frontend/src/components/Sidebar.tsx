import NewChatButton from "./NewChatButton";
import SearchIcon from "../assets/glasszoo1.svg"
import inboxicon from "../assets/inbox.svg"
import { useState } from "react";
import "./Sidebar.css";

const holder:React.CSSProperties={
  width: "100%",
  flex: 1,
  display: "flex",
  flexDirection: "row",
  alignItems: "flex-end",
  
}
function setClicks_search({
  setCheck,
  check,
  setMainWindow
}: {
  setCheck: React.Dispatch<React.SetStateAction<number>>;
  check: number;
  setMainWindow: React.Dispatch<React.SetStateAction<string>>;
}): void {
  // Example usage:
  if (check !== 1) {
    setMainWindow("search");
    setCheck(1);
  } else {
    setMainWindow("home");
    setCheck(0);
  }
}
function setClicks_inbox({
  setCheck,
  check,
  setMainWindow
}: {
  setCheck: React.Dispatch<React.SetStateAction<number>>;
  check: number;
  setMainWindow: React.Dispatch<React.SetStateAction<string>>;
}): void {
  // Example usage:
  if (check !== 2) {
    setMainWindow("inbox");
    setCheck(2);
  } else {
    setMainWindow("home");
    setCheck(0);
  }
}
export default function Sidebar({setmainwindow}:{
  setmainwindow:React.Dispatch<React.SetStateAction<string>>
}

) {
  const [check,setcheck]=useState(0);
  return (
    <div className="sidebar">
      <div className="sidebar-header" style={{width:"100%",height:"100px"}}>
        <h2>Chats</h2>
      </div>
      <NewChatButton />
      <div style={holder}>

       <button
          className="sidebar-bottom-btn"
          onClick={() =>
            setClicks_search({
              setCheck: setcheck,
              check: check,
              setMainWindow: setmainwindow,
            })
          }
        >
          <img src={SearchIcon} width={20} height={20} />
        </button>
        <button
          className="sidebar-bottom-btn"
          onClick={() =>
            setClicks_inbox({
              setCheck: setcheck,
              check: check,
              setMainWindow: setmainwindow,
            })
          }
        >
          <img src={inboxicon} width={25} height={25} />
        </button>

      </div>
    </div>
    
  );
}

import { useState } from "react";
import { type FormEvent, useRef } from "react";
import axios from 'axios';
import "./SearchFriends.css";

interface UserCardProps {
  username: string;     // The person found in search
  label: string;        // Their current status
  source: string;       // YOU (the logged-in user)
  setUsers: React.Dispatch<React.SetStateAction<Record<string, string>>>;
}

function UserCard({ username, label, source, setUsers }: UserCardProps) {
  const firstLetter = username.charAt(0).toUpperCase();

  const handleSendRequest = async (): Promise<void> => {
    try {
      await axios.post('http://127.0.0.1:8000/search/friends/send_request', {
        source: source,
        target: username
      });

      // Update the parent state immediately to change the UI
      setUsers((prev) => ({
        ...prev,
        [username]: "sent"
      }));
    } catch (error) {
      console.error("Error sending request", error);
    }
  };

  return (
    <div className="user-card">
      <div className="user-left">
        <div className="avatar">{firstLetter}</div>
        <span className="username">{username}</span>
      </div>

      <div className="user-right">
        {label === "sent" && <span className="status-badge requested">Requested</span>}
        {label === "friend" && <span className="status-badge friend">Friend</span>}
        {label === "unknown" && (
          <button className="send-btn" onClick={handleSendRequest}>
            Send Request
          </button>
        )}
      </div>
    </div>
  );
}
export default function SearchFriend({username}:{username:string}){

    const [users, setUsers] = useState<Record<string, string>>({});
    const usernameRef = useRef<HTMLInputElement>(null);
    const handleSubmit = async(e:FormEvent) =>{
      e.preventDefault();
        if(usernameRef.current==null){
          alert("enter a value");
          return;
        }
        const response=await axios.post('http://127.0.0.1:8000/search/users',{
                "query": usernameRef.current.value,
                "username":username
        });
        const allUsers = response.data.users;

          // Use destructuring to pull the logged-in user out of the object
          // 'username' here is the prop passed to SearchFriend (the logged-in user)
          const { [username]: removed, ...filteredUsers } = allUsers;

          setUsers(filteredUsers);

    }

   return (
          <div className="search-friend">
            <form onSubmit={handleSubmit}>
              <input
                type="text"
                ref={usernameRef}
                placeholder="Search username"
                className="search-input"
              />

              <button type="submit" className="search-btn">
                Search
              </button>
            </form>

            <div>
              {Object.entries(users).map(([user, label]) => (
                    <UserCard 
                      key={user} 
                      username={user} 
                      label={label} 
                      source={username}
                      setUsers={setUsers}
                    />
                  ))}
            </div>
          </div>
    );


}

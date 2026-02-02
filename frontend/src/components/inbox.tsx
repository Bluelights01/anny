import { useState, useEffect } from "react";
import axios from "axios";
import "./Inbox.css";

interface InboxProps {
  username: string;
}

export default function Inbox({ username }: InboxProps) {
  const [requests, setRequests] = useState<string[]>([]);

  useEffect(() => {
    const fetchRequests = async () => {
      if (!username) return;
      try {
        const response = await axios.post("https://anny-uro3.onrender.com/search/friends/read", {
          username: username,
          field:"requests"
        });
        if (response.data && response.data.data) {
          setRequests(response.data.data);
        }
      } catch (error) {
        console.error("Error fetching requests", error);
      }
    };
    fetchRequests();
  }, [username]);

  const handleAction = async (target: string, action: "accept" | "reject",source:string) => {
    try {
      await axios.post(`https://anny-uro3.onrender.com/search/friends/${action}_request`, {
        source: source,
        target: target,
      });
      setRequests((prev) => prev.filter((r) => r !== source));
    } catch (error) {
      console.error(`Error ${action}ing request`, error);
    }
  };

  return (
    <div className="inbox-container">
      <h2>Friend Requests</h2>
      <div className="requests-list">
        {requests.length === 0 ? (
          <p>No pending requests</p>
        ) : (
          requests.map((req) => (
            <div key={req} className="request-card">
              <div className="user-left">
                <div className="avatar">{req.charAt(0).toUpperCase()}</div>
                <span className="username">{req}</span>
              </div>
              <div className="user-right">
                <button
                  className="accept-btn"
                  onClick={() => handleAction(username, "accept",req)}
                >
                  Accept
                </button>
                <button
                  className="reject-btn"
                  onClick={() => handleAction(username, "reject",req)}
                >
                  Reject
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
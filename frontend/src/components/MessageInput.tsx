import { useState } from "react";
import "./MessageInput.css";

export default function MessageInput() {
  const [message, setMessage] = useState("");

  return (
    <div className="message-input">
      <input
        type="text"
        placeholder="Write a message..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button>Send</button>
    </div>
  );
}

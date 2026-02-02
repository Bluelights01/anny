/* Chat Window */
import React from "react";

const chat_window: React.CSSProperties = {
  flex: 1,
  padding: "16px",
  backgroundColor: "white",
  overflowY: "auto",
};
export default function ChatWindow() {
  return (
    <div style={chat_window}>
      <p style={{ color: "#999" }}>Start a conversation...</p>
    </div>
  );
}

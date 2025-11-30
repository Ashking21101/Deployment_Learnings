import { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);   // chat history
  const [loading, setLoading] = useState(false);  // typing indicator

  const sendQuestion = async () => {
    if (!question.trim()) return;

    // Add user message
    setMessages((prev) => [
      ...prev,
      { sender: "user", text: question, time: new Date().toLocaleTimeString() }
    ]);

    setLoading(true);

    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();

    // Add bot response
    setMessages((prev) => [
      ...prev,
      { sender: "bot", text: data.answer, time: new Date().toLocaleTimeString() }
    ]);

    setQuestion("");
    setLoading(false);

    // Scroll down after reply
    const chatBox = document.getElementById("chat-box");
    setTimeout(() => {
      chatBox.scrollTop = chatBox.scrollHeight;
    }, 50);

    // Auto focus again
    const input = document.getElementById("input-box");
    setTimeout(() => input.focus(), 50);
  };

  // Press Enter to send
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendQuestion();
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "40px auto", fontFamily: "Arial" }}>
      <h2 style={{ textAlign: "center" }}>Customer Support Chatbot</h2>

      <div
        id="chat-box"
        style={{
          background: "#f7f7f7",
          height: "400px",
          overflowY: "auto",
          padding: "15px",
          borderRadius: "8px",
          marginBottom: "15px",
          border: "1px solid #ddd"
        }}
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              textAlign: msg.sender === "user" ? "right" : "left",
              margin: "10px 0",
            }}
          >
            <span
              style={{
                display: "inline-block",
                padding: "10px 14px",
                borderRadius: "15px",
                background: msg.sender === "user" ? "#0084ff" : "#e3e3e3",
                color: msg.sender === "user" ? "white" : "black",
                maxWidth: "70%",
                textAlign: "left",
              }}
            >
              {msg.text}
              <div style={{ fontSize: "11px", opacity: 0.6, marginTop: "6px" }}>
                {msg.time}
              </div>
            </span>
          </div>
        ))}

        {loading && (
          <div style={{ marginTop: "8px", fontStyle: "italic", color: "gray" }}>
            Bot is typing...
          </div>
        )}
      </div>

      <textarea
        id="input-box"
        rows="3"
        style={{ width: "100%", padding: "10px" }}
        placeholder="Ask something about the product or support..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={handleKeyDown}
        autoFocus
      />

      <button
        onClick={sendQuestion}
        disabled={loading}
        style={{
          marginTop: "10px",
          padding: "10px 20px",
          background: loading ? "gray" : "black",
          color: "white",
          border: "none",
          cursor: loading ? "not-allowed" : "pointer",
          width: "100%",
          fontSize: "16px"
        }}
      >
        {loading ? "Please wait..." : "Send"}
      </button>
    </div>
  );
}

export default App;

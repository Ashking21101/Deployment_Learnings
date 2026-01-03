// Below code is to be used if we are using FETCH in service/api.js file instead of AXIOS API. 
import { useState } from "react";
import { apiPost } from "../services/api";
// apiPost is a helper that hides fetch logic

function Home() {
  // Stores user input text
  const [input, setInput] = useState("");

  // Stores reply returned from backend
  const [reply, setReply] = useState("");

  // Called when user clicks "Send"
  const sendMessage = async () => {
    try {
      // Frontend → backend POST request starts here
      const data = await apiPost("/chat", {
        message: input, // JSON sent to FastAPI
      });

      // Update UI with backend response
      setReply(data.reply);
    } catch (err) {
      console.error(err);
      setReply("Error talking to backend");
    }
  };

  return (
    <div>
      {/* User input field */}
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type message"
      />

      {/* Triggers sendMessage */}
      <button onClick={sendMessage}>Send</button>

      {/* Displays LLM response */}
      <p>{reply}</p>
    </div>
  );
}

export default Home;








/* below code is to be used if we are using AXIOS in service/api.js file instead of fetch API. 
import { useState } from "react";
import { api } from "../services/api";

function Home() {
  const [input, setInput] = useState("");
  const [reply, setReply] = useState("");

  const sendMessage = async () => {
    try {
      const response = await api.post("/chat", {
        message: input,
      });
      setReply(response.data.reply);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{ padding: "1rem" }}>
      <h1>Chat</h1>

      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type message"
      />

      <button onClick={sendMessage}>Send</button>

      <p>{reply}</p>
    </div>
  );
}

export default Home;
*/






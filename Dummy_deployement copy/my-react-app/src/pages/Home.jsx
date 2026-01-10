import { useState } from "react";
// Clerk hook to access authentication utilities (JWT, user info, etc.)
import { useAuth } from "@clerk/clerk-react";
import { apiPost } from "../services/api";



function Home() {
  // Holds the text typed by the user in the input box
  const [input, setInput] = useState("");
  // Holds the reply returned by FastAPI (LLM response)
  const [reply, setReply] = useState("");

  // getToken() returns the logged-in user's JWT from Clerk
  // This JWT proves WHO the user is
  const { getToken } = useAuth();

  // Called when user clicks the "Send" button
  const sendMessage = async () => {
    try {
      // 1️⃣ Ask Clerk for a valid JWT for the current user
      const token = await getToken();

      // 2️⃣ Send POST request to FastAPI
      //    - "/chat" → FastAPI endpoint
      //    - { message: input } → request body
      //    - token → Authorization header (Bearer token)
      const data = await apiPost(
        "/chat",
        { message: input },
        token
      );

      // 3️⃣ Update UI with response returned by backend
      setReply(data.reply);
    } catch (err) {
      // If backend is down / token invalid / network error
      console.error(err);
      setReply("Error talking to backend");
    }
  };

  return (
    <div>
      {/* Text input controlled by React state */}
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)} // updates `input`
        placeholder="Type message"
      />

      {/* Triggers backend call */}
      <button onClick={sendMessage}>Send</button>

      {/* Displays LLM response */}
      <p>{reply}</p>
    </div>
  );
}

export default Home;





/* before code clerk integration
import { useState } from "react";
import { apiPost } from "../services/api";

function Home() {
  const [input, setInput] = useState("");
  const [reply, setReply] = useState("");

  const sendMessage = async () => {
    try {
      const data = await apiPost("/chat", {
        message: input, /
      });

      setReply(data.reply);
    } catch (err) {
      console.error(err);
      setReply("Error talking to backend");
    }
  };
  return (
    <div>
      // User input field 
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
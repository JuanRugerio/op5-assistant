import { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import InputBox from "./components/InputBox";
import { sendMessage } from "./api";

//App is the Root. Stores entire conversation. Triggered when user submits input. Create message 
//object. Updates UI with user message. Calls backend API. Display answer. Handles sources. 
//UI Rendering, Title, Passes all messages to display component. 
function App() {
  const [messages, setMessages] = useState([]);

  const handleSend = async (text) => {
    const userMessage = { role: "user", text };
    setMessages((prev) => [...prev, userMessage]);

    const response = await sendMessage(text);

    const botMessage = {
      role: "assistant",
      text: response.answer || "No response",
    };

    const sourcesMessage = response.citations?.length
    ? {
        role: "assistant",
        text:
            "Sources:\n" +
            response.citations
            .map((c) => `Page ${c.page}: "${c.quote}"`)
            .join("\n"),
        }
    : null;

    setMessages((prev) => [
        ...prev,
        botMessage,
        ...(sourcesMessage ? [sourcesMessage] : []),
    ]);
}; 

  return (
    <div style={{ maxWidth: "600px", margin: "auto", marginTop: "50px" }}>
      <h2>Omnipod 5 Assistant</h2>
      <ChatWindow messages={messages} />
      <InputBox onSend={handleSend} />
    </div>
  );
}

export default App;

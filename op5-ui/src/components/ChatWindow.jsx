import Message from "./Message";

export default function ChatWindow({ messages }) {
  return (
    <div style={{ height: "400px", overflowY: "auto", border: "1px solid #ccc", padding: "10px" }}>
      {messages.map((msg, idx) => (
        <Message key={idx} role={msg.role} text={msg.text} />
      ))}
    </div>
  );
}

//Display conversation history. It does not manage state. Receives messages, loops through them and 
//Renders each one using a Message component. 
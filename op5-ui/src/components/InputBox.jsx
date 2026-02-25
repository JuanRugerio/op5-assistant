import { useState } from "react";

export default function InputBox({ onSend }) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    onSend(input);
    setInput("");
  };

  return (
    <div style={{ display: "flex", marginTop: "10px" }}>
      <input
        style={{ flex: 1, padding: "10px" }}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask about Omnipod 5..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}

//Captures user input.  Updates text as user types. Sends message to parent. Clears input after sending
//Import React´s state hook, to let the component remember what the user is typing. 
//Component definition, Triggers backend pipeline. State variable, current text in the box and 
//function to update it. Initial value empty string. Running function when user clicks send. 
//Remove spaces, call function from App.jsx. Clear input. Horizontal layout, input + button side by 
//side. Spacing from chat window. Input box always reflects React state. Every keystroke, updates 
//state and re renders input. Button triggers handleSend to send message to backend.
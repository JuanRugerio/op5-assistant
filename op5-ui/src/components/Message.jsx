export default function Message({ role, text }) {
  return (
    <div style={{
      textAlign: role === "user" ? "right" : "left",
      margin: "10px"
    }}>
      <div style={{
        display: "inline-block",
        padding: "10px",
        borderRadius: "10px",
        background: role === "user" ? "#DCF8C6" : "#EEE"
      }}>
        {text}
      </div>
    </div>
  );
}

// Renders a single chat message. Component definiton. Control positioning of the message. If user,
//align right, if assistant, align left. Make the bubble wrap tightly around the text. Space inside
//bubble. Rounded corners. Background colors. Inser the actual message string. 
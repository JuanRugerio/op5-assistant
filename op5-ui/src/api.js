const API_URL = "http://localhost:8000/chat";

export async function sendMessage(message) {
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        session_id: "default-session",
        message: message,
      }),
    });

    if (!response.ok) {
      throw new Error("API error");
    }

    return await response.json();
  } catch (error) {
    return {
      answer: "⚠️ Error contacting backend.",
      citations: [],
    };
  }
}


//Function sending POST request to FastAPI backend. Wait for response. Returns parsed JSON. Handles
//errors gracefully. async allows await. message is user input string. export lets other files use it
//try handles possible failures. fetch built in browser function for HTTP requests. await pauses
//until response arrives. Sending data. Tell backend JSON data is being sent. Convert JS object into
//JSON string. Check fro HTTP errors. Convert backend JSON into JS object. Error handling. 
//Fallback response. 
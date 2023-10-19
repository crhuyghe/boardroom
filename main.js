import "JSON Templates"

const ws = new WebSocket("ws://localhost:8765")

ws.onopen = event =>  // Send a message to the server upon initial opening of the socket.
{
    alert("Connection established.")
    alert("Sending message to server...")
    ws.send("This message has been sent to the server.")
}


// ws.close()  // Close the socket.





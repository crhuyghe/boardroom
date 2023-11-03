// import "JSON Templates"

const ws = new WebSocket("ws://localhost:8765")

ws.onopen = event =>  // Send a message to the server upon initial opening of the socket.
{
    console.log("Connection established.")
    console.log("Sending message to server...")
    ws.send(JSON.stringify({"action": 1}))
}

ws.onerror = error =>
{
    console.error(error)
}

ws.onmessage = event =>
{
    console.log(event.data)
}
// ws.close()  // Close the socket.





//var ws = new WebSocket("ws://localhost:8000/ws");
var ws = new WebSocket("wss://art-intel.site/ws");

var startTime;

ws.onmessage = function(event) {
    var rtt = new Date() - startTime;
    var messages = document.getElementById('messages')
    var message = document.createElement('li')
    var content = document.createTextNode(event.data)
    content += "RTT: " + rtt;
    message.appendChild(content)
    messages.appendChild(message)
};

function sendMessage(event) {
   var input = document.getElementById("messageText")
   startTime = new Date();
   ws.send(input.value)
   input.value = ''
   event.preventDefault()
}
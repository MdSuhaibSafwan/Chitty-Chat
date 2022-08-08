var loc = location;

var protocol = "ws:"
if (loc.protocol == "https:"){
    protocol = "wss:"
};

var auth_token = token;

url = `${protocol}//${loc.host}/room/?token=${auth_token}`;

var socket = new WebSocket(url);

socket.onopen = function(e){
    console.log(e)
};

socket.onerror = function(e){
    console.log(e);
};

socket.onclose = function(e){
    console.log(e);
};

socket.onmessage = function(e){
    var data = JSON.parse(e.data);
    console.log(data);
};

var btn = document.getElementById("btn-send");
console.log(btn);
btn.addEventListener("click", (e) => {
    socket.send(JSON.stringify({
        "command": "new_message",
        "text": "hello",
        "user": "2",
    }))
})




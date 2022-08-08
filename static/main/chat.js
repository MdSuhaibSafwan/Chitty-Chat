var loc = location;

var protocol = "ws:"
if (loc.protocol == "https:"){
    protocol = "wss:"
};

var auth_token = token;

url = `${protocol}//${loc.host}/room/?token=${auth_token}`;

var socket = new WebSocket(url);

socket.onmessage = function(e){
    console.log(e);
};

socket.onopen = function(e){
    console.log(e)
};

socket.onerror = function(e){
    console.log(e);
};

socket.onclose = function(e){
    console.log(e);
};

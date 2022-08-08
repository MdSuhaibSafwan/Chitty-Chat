// socket.send({
//     "command": "new_message",
//     "text": "hello",
// })

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




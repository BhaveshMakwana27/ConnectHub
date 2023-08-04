function scrollToBottom() {
    const chatContainer = document.getElementById("chat-container");
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Call the function initially and after new messages are added
scrollToBottom();


const roomName = JSON.parse(document.getElementById('room_name').innerText);
const userName = JSON.parse(document.getElementById('curr_username').innerText);
const receiverName = JSON.parse(document.getElementById('receiver_username').innerText);
const encodedRoomName = encodeURIComponent(roomName);
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/messaging/do_message/'
    + encodedRoomName
    + '/'
);

// whenever the message is sent the message will be received here
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    let currTime = new Date()
    let ampm = currTime.getHours()<12 ? 'a.m.':'p.m.'
    if(data.username == data.receiver){
        document.querySelector('#chat-container').innerHTML = document.querySelector('#chat-container').innerHTML+  
                        ` <div class="row justify-content-start receivedMessage text-start mt-2">
                                    <span>${data.message}<i class='timeStamp'>${currTime.getHours()}:${currTime.getMinutes()} ${ampm}</i></span>
                          </div>
                        `
    }else{
        document.querySelector('#chat-container').innerHTML = document.querySelector('#chat-container').innerHTML+  
                        `<div class="row justify-content-start sendMessage text-end mt-2">
                                    <span>${data.message}<i class='timeStamp'>${currTime.getHours()}:${currTime.getMinutes()} ${ampm}</i></span>
                            </div>
                        `

    }
    scrollToBottom();
};

chatSocket.onclose = function (e) {
    console.log('onclose');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.key === 'Enter') {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': userName,
        'receiver': receiverName
    }));
    messageInputDom.value = '';
};



document.getElementById('visitProfile').onclick = ()=>{
    window.location.href = `/followers/visit_profile/${receiverName}`
}
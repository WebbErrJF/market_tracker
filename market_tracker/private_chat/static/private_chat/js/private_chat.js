document.addEventListener('DOMContentLoaded', () => {
        const logged_user = JSON.parse(document.getElementById('logged_user').textContent);
        const contactItems_1 = document.querySelectorAll('#contacts li');
        const passed_user = JSON.parse(document.getElementById('passed_user').textContent);
        const otherUserIdPlaceholder = document.getElementById('otherUserIdPlaceholder');
        if (passed_user ) {
            otherUserId = passed_user;
            contactItems_1.forEach(contactItem => {
                if (otherUserId.toString() === contactItem.id) {
                    otherUserIdPlaceholder.textContent = contactItem.textContent;
                }
            })

        }
        else {
            otherUserId = contactItems_1[0].id;
            otherUserIdPlaceholder.textContent = contactItems_1[0].textContent;
        }
        const chatSocket = new WebSocket(getWebSocketURL(otherUserId, logged_user));
        const chatList = document.querySelector('#chat');
        let contactItems = document.querySelectorAll('#contacts li');
        const messageInputDom = document.querySelector('#chat-message-input');
        const messageSubmitButton = document.querySelector('#chat-message-submit');


        contactItems.forEach((contactItem) => {
            contactItem.addEventListener('click', () => {
                const contactName = contactItem.id;
                if (otherUserId !== contactName) {
                    otherUserId = contactName;
                    while (chatList.firstChild) {
                        chatList.removeChild(chatList.firstChild);
                    }
                    chatSocket.send(JSON.stringify({
                        'type': 'change_contact',
                        'change_contact': contactName
                    }));
                    otherUserIdPlaceholder.textContent = contactItem.textContent;
                }
            });
        });


        chatSocket.onmessage = function (e) {
            const data = JSON.parse(e.data);
            if (data.type === "chat.history") {
                data.messages.forEach((message) => {
                    appendMessageToChatList(message, data.logged_user, chatList);
                });
            } else {
                appendMessageToChatList(data, data.logged_user, chatList);
            }
        };

        chatSocket.onclose = function (e) {
            console.error('Chat socket closed unexpectedly');
        };

        messageInputDom.focus();

        messageInputDom.onkeyup = function (e) {
            if (e.key === 'Enter') {
                messageSubmitButton.click();
            }
        };

        messageSubmitButton.onclick = function () {
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'type': 'message',
                'message': message
            }));
            messageInputDom.value = '';
        };

        function getWebSocketURL(otherUserId, logged_user) {
            return `ws://${window.location.host}/ws/chat/${otherUserId}/${logged_user}/`;
        }

        function appendMessageToChatList(message, loggedUser, chatList) {
            const newMessage = document.createElement('li');
            const status = message.username === loggedUser ? 'blue' : 'green';
            const messageHTML = `
                <div class="entete">
                    <h3>${message.formatted_time_stamp}</h3>
                    <h2>${message.username}</h2>
                    <span class="status ${status}"></span>
                </div>
                <div class="message">${message.message}</div>`;
            newMessage.innerHTML = messageHTML;
            newMessage.classList.add(message.username === loggedUser ? 'me' : 'you');
            chatList.appendChild(newMessage);
            chatList.scrollTop = chatList.scrollHeight;
        }
});
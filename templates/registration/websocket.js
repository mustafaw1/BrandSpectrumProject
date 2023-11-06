// websocket.js

document.addEventListener("DOMContentLoaded", function () {
  const username = "{{ user.username }}"; // Get the username of the current user

  const chatSocket = new WebSocket(
    "ws://" + window.location.host + `/ws/messaging/${username}/`
  );

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const message = data.message;
    const senderUsername = data.sender_username;

    // Handle incoming message - display it in the chat container
    // You can customize how the message is rendered here
    const messageElement = document.createElement("p");
    messageElement.textContent = `${senderUsername}: ${message}`;
    const chatBox = document.getElementById("chat-box");
    chatBox.appendChild(messageElement);
  };

  const messageForm = document.getElementById("message-form");
  const messageInput = document.getElementById("message-input");

  messageForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const message = messageInput.value;
    chatSocket.send(JSON.stringify({ message: message }));

    messageInput.value = "";
  });
});

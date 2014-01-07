// Shitty code is shitty, but fuck it!

var SERVER_HOST = "localhost";
var SERVER_PORT = 9000;

var socket;

window.onload = function () {
  socket = new WebSocket("ws://" + SERVER_HOST + ":" + SERVER_PORT + "/");

  // Receive data from the server
  socket.onmessage = function (evt) {
    console.log(JSON.parse(evt.data));
  };
};
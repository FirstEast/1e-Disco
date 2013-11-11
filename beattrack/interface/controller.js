// Shitty code is shitty, but fuck it!

var SERVER_HOST = "localhost";
var SERVER_PORT = 2000;

var count = 0;

var socket;

window.onload = function () {
  socket = new WebSocket("ws://" + SERVER_HOST + ":" + SERVER_PORT + "/");

  // Receive data from the server
  socket.onmessage = function (evt) {
    count++
    var data = JSON.parse(evt.data);
    
    if ($(".bar").length == 0) {
      buildBars(data);
    }

    if (count >= 3) {
      updateBars(data);
      count = 0;
    }
  };
};

buildBars = function(data) {
  var width = Math.floor(100 / data.length) + "%";
  for (var i = 0; i < data.length; i++) {
    $("body").append($("<div class='bar'/>").css("width", width));
  }
}

updateBars = function(data) {
  $bars = $(".bar");
  for (var i = 0; i < data.length; i++) {
    $($bars[i]).css("height", (data[i] / 1000) + "px"); 
  }
}
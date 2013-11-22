// Shitty code is shitty, but fuck it!

var SERVER_HOST = "localhost";
var SERVER_PORT = 3333;

var LENGTH = 200

var squarePx;

var context;

var socket;

window.onload = function () {
  var white = [];
  for(var i = 0; i < LENGTH; i++) {
    white.push(255);
    white.push(255);
    white.push(255);
  }

  calculateCanvas();
  colorCanvas(white);

  socket = new WebSocket("ws://" + SERVER_HOST + ":" + SERVER_PORT + "/");

  // Receive data from the server
  socket.onmessage = function (evt) {
    colorCanvas(JSON.parse(evt.data));
    socket.send("OK");
  };
};

calculateCanvas = function() {
  var $canvas = $("canvas");
  var canvas = $canvas[0];
  context = canvas.getContext('2d');

  canvas.width = $("body").width();
  canvas.height = $("body").height();

  squarePx = ((canvas.width/LENGTH) | 0) - 1;
}

colorCanvas = function(RGBArray) {
  for (var i = 0; i < LENGTH; i++) {
    var red = RGBArray[i*3];
    var green = RGBArray[i*3 + 1];
    var blue = RGBArray[i*3 + 2];
    context.fillStyle = "rgb(" + red + "," + green + "," + blue + ")";
    context.fillRect(i*(squarePx + 1), 20, squarePx, squarePx);

    context.fillRect(i*(squarePx + 1), 100, squarePx, squarePx);
  }
}
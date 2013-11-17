// Shitty code is shitty, but fuck it!

var SERVER_HOST = "localhost";
var SERVER_PORT = 2222;

var WIDTH = 48
var HEIGHT = 24

var squareWidthPx;
var squareHeightPx;

var context;

var socket;

window.onload = function () {
  var white = [];
  for(var i = 0; i < HEIGHT; i++) {
    for (var j = 0; j < WIDTH; j++) {
      white.push(255);
      white.push(255);
      white.push(255);
    }
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

  squarePx = ((canvas.width/WIDTH) | 0) - 5;
}

colorCanvas = function(RGBArray) {
  for (var i = 0; i < HEIGHT; i++) {
    for (var j = 0; j < WIDTH; j++) {
      var red = RGBArray[(i * WIDTH + j)*3];
      var green = RGBArray[(i * WIDTH + j)*3 + 1];
      var blue = RGBArray[(i * WIDTH + j)*3 + 2];
      context.fillStyle = "rgb(" + red + "," + green + "," + blue + ")";
      context.fillRect(j*(squarePx + 1), i*(squarePx + 1), squarePx, squarePx);
    }
  }
}
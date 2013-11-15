// Shitty code is shitty, but fuck it!

var SERVER_HOST = "localhost";
var SERVER_PORT = 1111;

var WIDTH = 160
var HEIGHT = 110

var squareWidthPx;
var squareHeightPx;

var context;

var socket;

window.onload = function () {
  var white = [];
  for(var i = 0; i < 1185; i++) {
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

  squareWidthPx = ((canvas.width/WIDTH) | 0) - 1;
  squareHeightPx = ((canvas.height/HEIGHT) | 0) - 1;
}

colorCanvas = function(RGBArray) {
  for (var i = 0; i < 395; i++) {
    var coords = getCoordFromIndex(i);
    var red = RGBArray[i * 3];
    var green = RGBArray[i * 3 + 1];
    var blue = RGBArray[i * 3 + 2];
    context.fillStyle = "rgb(" + red + "," + green + "," + blue + ")";
    context.fillRect(coords[0]*(squareWidthPx + 1), coords[1]*(squareHeightPx + 1), squareWidthPx, squareHeightPx);
  }
}

// Modifying this function will result in instantaneous death.
getCoordFromIndex = function(index) {
  var i, j;
  if (index < 160) {
    i = WIDTH - index - 1;
    j = HEIGHT;
  } else if (index == 160) {
    i = 0;
    j = HEIGHT - 1;
  } else if (index == 161) {
    i = 0;
    j = HEIGHT - 2;
  } else if (index > 161 && index <= 208) {
    i = 0;
    j = (HEIGHT - 50) - (index - 161) - 1;
  } else if (index > 208 && index <= 222) {
    i = (index - 208)
    j = (HEIGHT - 50) - (208 - 161) - 1;
  } else if (index > 222 && index <= 235) {
    i = 222 - 208;
    j = (HEIGHT - 50) - (index - 175) - 1;
  } else if (index > 235 && index <= 366) {
    i = index - 222;
    j = 0;
  } else if (index > 366 && index <= 380) {
    i = 366 - 222;
    j = index - 366;
  } else if (index > 380 && index <= 394) {
    i = index - 236;
    j = 380 - 366;
  } else {
    i = 159;
    j = 13;
  }

  return [i, j];
}
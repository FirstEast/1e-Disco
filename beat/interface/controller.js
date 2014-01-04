// Shitty code is shitty, but fuck it!

var SERVER_HOST = "localhost";
var SERVER_PORT = 2000;

var socket;

window.onload = function () {
  socket = new WebSocket("ws://" + SERVER_HOST + ":" + SERVER_PORT + "/");

  // Receive data from the server
  socket.onmessage = function (evt) {
    var data = JSON.parse(evt.data);

    updateVolume(data);
    updateCentroid(data);

    if ($('.bar').length == 0) {
      buildBars(data.leftFrequencies);
    }

    updateBars(data.leftFrequencies);
  };
};

updateVolume = function(data) {
  var avgVol = (data.leftVolume + data.rightVolume) / 2;
  $('.volume').height(((avgVol * 100) + 1) + '%');
}

updateCentroid = function(data) {
  var avgCentroid = (data.leftCentroid + data.rightCentroid) / 2
  $('.centroid').height(((avgCentroid * 100) + 1) + '%');
}

buildBars = function(freqs) {
  var width = Math.floor(100 / freqs.length) + '%';
  for (var i = 0; i < freqs.length; i++) {
    $('.bar-container').append($("<div class='bar'/>").css('width', width));
  }
}

updateBars = function(freqs) {
  $bars = $('.bar');
  for (var i = 0; i < freqs.length; i++) {
    $($bars[i]).css('height', (Math.max(freqs[i],1)) + 'px'); 
  }
}
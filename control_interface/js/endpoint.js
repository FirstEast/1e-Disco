(function() {
  var _this = this;

  com.firsteast.WEBSOCKET_URL = window.location.origin.split('//')[1].split(':')[0];

  com.firsteast.WEBSOCKET_PORT = '9000';

  com.firsteast.OUTPUT_DEVICES = ['ddf', 'goodale', 'bemis'];

  com.firsteast.INPUT_DEVICES = ['beat'];

  com.firsteast.DDF_WIDTH = 48;

  com.firsteast.DDF_HEIGHT = 24;

  com.firsteast.BEMIS_WIDTH = 264;

  com.firsteast.GOODALE_CANVAS_WIDTH = 160;

  com.firsteast.GOODALE_CANVAS_HEIGHT = 110;

  com.firsteast.GOODALE_WIDTH = 395;

  $('document').ready((function() {
    var controller, mockPreviewArea, previewArea, session, sideMenu;
    session = new com.firsteast.DiscoSession();
    controller = new com.firsteast.DiscoController({
      session: session
    });
    previewArea = new com.firsteast.PreviewArea({
      model: session.realDiscoModel,
      session: session,
      isMock: false
    });
    previewArea.render();
    $('.previews').append(previewArea.$el);
    mockPreviewArea = new com.firsteast.PreviewArea({
      model: session.mockDiscoModel,
      session: session,
      isMock: true
    });
    mockPreviewArea.render();
    $('.previews').append(mockPreviewArea.$el);
    sideMenu = new com.firsteast.SideMenu({
      el: $('.menu'),
      model: session.displayModel,
      realDiscoModel: session.realDiscoModel,
      mockDiscoModel: session.mockDiscoModel
    });
    return sideMenu.render();
  }));

}).call(this);

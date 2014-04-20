(function() {
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

  $('document').ready(((function(_this) {
    return function() {
      var beatPreview, controller, mockPreviewArea, navbar, previewArea, session, sideMenu;
      session = new com.firsteast.DiscoSession();
      controller = new com.firsteast.DiscoController({
        session: session
      });
      navbar = new com.firsteast.NavBar({
        el: $('.nav-bar')
      });
      navbar.render();
      sideMenu = new com.firsteast.SideMenu({
        el: $('.side-menu'),
        model: session.displayModel,
        realDiscoModel: session.realDiscoModel,
        mockDiscoModel: session.mockDiscoModel,
        hotkeyModel: session.hotkeyModel,
        savedPatternList: session.savedPatternList
      });
      sideMenu.render();
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
      beatPreview = new com.firsteast.BeatPreview({
        model: session.beatModel
      });
      beatPreview.render();
      return $('.content-area').append(beatPreview.$el);
    };
  })(this)));

}).call(this);

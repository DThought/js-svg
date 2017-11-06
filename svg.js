function Svg(target) {
  var self = this;

  this.render = function(url) {
    $.get(url, self.renderXml);
  }

  this.renderXml = function(xml) {
    var height = xml.documentElement.getAttribute('height');
    var width = xml.documentElement.getAttribute('width');
    var nodes = xml.domElement.children;

    $target = $(target).addClass('svg').empty();

    for (var i = 0; i < nodes.length; i++) {
      switch (node.tagName) {
        case 'ellipse':
          break;
        case 'line':
          break;
      }
    }
  }
}

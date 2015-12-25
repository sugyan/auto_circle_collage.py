'use strict';

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/* global $ */

var Main = (function () {
    function Main(canvas) {
        var _this = this;

        _classCallCheck(this, Main);

        this.width = canvas.width;
        this.height = canvas.height;
        this.ctx = canvas.getContext('2d');
        this.img = new Image();
        this.img.onload = function () {
            var scale = Math.max(_this.img.width / _this.width, _this.img.height / _this.height);
            var w = _this.img.width / scale;
            var h = _this.img.height / scale;
            var offset_x = (_this.width - w) / 2.0;
            var offset_y = (_this.width - h) / 2.0;
            _this.ctx.fillRect(0, 0, _this.width, _this.height);
            _this.ctx.drawImage(_this.img, offset_x, offset_y, w, h);
            window.setTimeout(function () {
                $.ajax({
                    url: '/api',
                    data: { url: _this.url },
                    success: function success(result) {
                        if (result.url != _this.url) {
                            return;
                        }
                        if (result.image) {
                            _this.img.src = result.image;
                        }
                    }
                });
            }, 2000);
        };
    }

    _createClass(Main, [{
        key: 'setUrl',
        value: function setUrl(url) {
            this.img.src = this.url = url;
        }
    }]);

    return Main;
})();

$(function () {
    var main = new Main(document.getElementById('canvas'));
    $('#url').submit(function () {
        var url = $('input[name="image_url"]').val();
        if (url) {
            main.setUrl(url);
        }
        return false;
    });
});
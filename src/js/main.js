/* global $ */

class Main {
    constructor(canvas) {
        this.width  = canvas.width;
        this.height = canvas.height;
        this.ctx = canvas.getContext('2d');
        this.img = new Image();
        this.img.onload = () => {
            const scale = Math.max(this.img.width / this.width, this.img.height / this.height);
            const w = this.img.width  / scale;
            const h = this.img.height / scale;
            const offset_x = (this.width - w) / 2.0;
            const offset_y = (this.width - h) / 2.0;
            this.ctx.fillRect(0, 0, this.width, this.height);
            this.ctx.drawImage(this.img, offset_x, offset_y, w, h);
            window.setTimeout(() => {
                $.ajax({
                    url: '/api',
                    data: { url: this.url },
                    success: (result) => {
                        if (result.url != this.url) {
                            return;
                        }
                        if (result.image) {
                            this.img.src = result.image;
                        }
                    }
                });
            }, 2000);
        };
    }
    setUrl(url) {
        this.img.src = this.url = url;
    }
}

$(() => {
    const main = new Main(document.getElementById('canvas'));
    $('#url').submit(() => {
        const url = $('input[name="image_url"]').val();
        if (url) {
            main.setUrl(url);
        }
        return false;
    });
});

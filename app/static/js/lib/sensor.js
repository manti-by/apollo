class Sensor {
    constructor(canvas, options = {}) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');

        this.color = 'color' in options ?
            options['color'] : 'rgba(165, 42, 42, 1)';

        this.fgcolor = 'fgcolor' in options ?
            options['fgcolor'] : 'rgba(165, 42, 42, .2)';

        this.bgcolor = 'bgcolor' in options ?
            options['bgcolor'] : 'rgba(255, 255, 255, 1)';

        this.unit = 'unit' in options ?
            options['unit'] : '';

        this.font = 'font' in options ?
            options['font'] : '20px Open Sans';

        this.font_color = 'font_color' in options ?
            options['font_color'] : 'rgba(0, 0, 0, .9)';
    }

    draw (value) {
        let cX = Math.floor(this.canvas.width / 2),
            cY = Math.floor(this.canvas.height / 2),
            radius = Math.min(cX, cY),
            offset = 90 * Math.PI / 180,
            radians = value / 100 * 360 * Math.PI / 180 - offset;

        this.ctx.fillStyle = this.bgcolor;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.draw_sector(cX, cY, radius, -offset, radians, this.color);
        this.draw_sector(cX, cY, radius, radians, 360 * Math.PI / 180, this.fgcolor);
        this.draw_sector(cX, cY, radius * .7, 0, 360 * Math.PI / 180, this.bgcolor);

        this.draw_label(cX, cY, value);
    }

    draw_sector (cX, cY, radius, start, stop, color) {
        this.ctx.fillStyle = color;
        this.ctx.beginPath();
        this.ctx.moveTo(cX, cY);
        this.ctx.arc(cX, cY, radius, start, stop);
        this.ctx.closePath();
        this.ctx.fill();
    }

    draw_label(cX, cY, text) {
        this.ctx.textAlign = 'center';
        this.ctx.font = this.font;
        this.ctx.fillStyle = this.font_color;
        this.ctx.fillText(text + this.unit, cX, cY + 5);
    }
}

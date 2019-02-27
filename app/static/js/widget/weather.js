(($) => {

    'use strict';

    class WeatherWidget {

        constructor() {
            this.directions = [
                "N", "NNE", "NE", "ENE",
                "E","ESE", "SE", "SSE",
                "S", "SSW", "SW", "WSW",
                "W", "WNW", "NW", "NNW"
            ];

            this.template = Handlebars.compile(
                $('#t-weather').html()
            );

            this.canvas = $('#weather');
        }

        init() {
            this.update();

            setInterval(
                () => this.update(), 5 * 60 * 1000
            );
        }

        deg_to_dir (deg) {
            let index = Math.floor(((deg / 22.5) + 0.5) % 16);
            return this.directions[index];
        };

        update() {
            $.getJSON(
                'https://api.openweathermap.org/data/2.5/weather?q=Minsk,by&units=metric&appid=aec9289a4fe49b1bca7296d08c1e170b',
                (data) => {
                    this.canvas.html(
                        this.template({
                            temp: data['main']['temp'],
                            wind: data['wind']['speed'],
                            wind_dir: this.deg_to_dir(data['wind']['deg']),
                            pressure: data['main']['pressure'],
                            icon: 'http://openweathermap.org/img/w/' + data['weather'][0]['icon'] + '.png'
                        })
                    );
                }
            )
        };
    }

    $.weather = new WeatherWidget();

})(jQuery);
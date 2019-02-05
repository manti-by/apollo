(($) => {

    'use strict';

    let directions = [
        "N", "NNE", "NE", "ENE",
        "E","ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW",
        "W", "WNW", "NW", "NNW"];

    let deg_to_dir = (deg) => {
        let index = Math.floor(((deg / 22.5) + 0.5) % 16);
        return directions[index];
    };

    let get_weather_data = () => {
        let template = Handlebars.compile($('#t-weather').html());
        $.getJSON(
            'https://api.openweathermap.org/data/2.5/weather?q=Minsk,by&units=metric&appid=aec9289a4fe49b1bca7296d08c1e170b',
            (data) => {
                $('#weather').html(template({
                        temp: data['main']['temp'],
                        wind: data['wind']['speed'],
                        wind_dir: deg_to_dir(data['wind']['deg']),
                        pressure: data['main']['pressure'],
                        icon: 'http://openweathermap.org/img/w/' + data['weather'][0]['icon'] + '.png'
                    })
                );
            }
        )
    };

    get_weather_data();
    setInterval(get_weather_data, 5 * 60 * 1000);

})(jQuery);
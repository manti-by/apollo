(($) => {

    'use strict';

    let get_weather_data = () => {
        $.getJSON(
            'https://api.openweathermap.org/data/2.5/weather?q=Minsk,by&units=metric&appid=aec9289a4fe49b1bca7296d08c1e170b',
            (data) => {
                $('#weather').html('<div>Temp: ' + data['main']['temp'] + 'C, pressure: ' + data['main']['pressure']);
            }
        )
    };

    get_weather_data();
    setInterval(get_weather_data, 5 * 60 * 1000);

})(jQuery);
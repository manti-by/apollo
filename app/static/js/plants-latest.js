(($) => {

    'use strict';

    class PlantsLatestWidget {
        constructor() {
            this.status = $('#status');
            this.temp = $('#plants-latest-temp').get(0);
            this.humidity = $('#plants-latest-humidity').get(0);
            this.moisture = $('#plants-latest-moisture').get(0);
        }

        init() {
            this.temp_chart = new Sensor(this.temp, {
                color: 'rgba(255, 99, 132, 1)',
                fgcolor: 'rgba(255, 99, 132, .2)',
                unit: '°C'
            });
            this.humidity_chart = new Sensor(this.humidity, {
                color: 'rgba(54, 162, 235, 1)',
                fgcolor: 'rgba(54, 162, 235, .2)',
                unit: '%'
            });
            this.moisture_chart = new Sensor(this.moisture, {
                color: 'rgba(153, 102, 255, 1)',
                fgcolor: 'rgba(153, 102, 255, .2)',
                unit: '%'
            });

            this.update();
            setInterval(
                () => this.update(),
                5 * 60 * 1000
            );
        }

        update() {
            $.getJSON('/api?limit=1', (data) => {
                this.temp_chart.draw(data['temp'][0]);
                this.humidity_chart.draw(data['humidity'][0]);
                this.moisture_chart.draw(data['moisture'][0]);
            }).done(() => {
                let now = new Date();

                this.status
                    .removeClass('text-danger')
                    .addClass('text-secondary')
                    .text(
                        'Last update: ' + now.getHours() + ':' + now.getMinutes()
                    );
            }).fail(() => {
                this.status
                    .removeClass('text-secondary')
                    .addClass('text-danger')
                    .text('Connection error');
            });
        }

    }

    $.plants_latest = new PlantsLatestWidget();

})(jQuery);
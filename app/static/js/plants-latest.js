(($) => {

    'use strict';

    class PlantsLatestWidget {
        constructor() {
            this.status = $('#status');
            this.temp = $('#plants-latest-temp');
            this.humidity = $('#plants-latest-humidity');
            this.moisture = $('#plants-latest-moisture');
        }

        init() {
            this.temp_chart = new Chart(this.temp, {
                type: 'doughnut',
                data: {
                    labels: ['Current Temperature'],
                    datasets: [{
                        data: [0, 100],
                        backgroundColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, .2)'
                        ]
                    }]
                },
                options: {
                    title: {
                        display: true,
                        position: 'bottom',
                        text: 'Temperature, C',
                    }
                },
            });

            this.humidity_chart = new Chart(this.humidity, {
                type: 'doughnut',
                data: {
                    labels: ['Humidity', 'Max'],
                    datasets: [{
                        data: [0, 100],
                        backgroundColor: [
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, .2)'
                        ]
                    }]
                },
                options: {
                    title: {
                        display: true,
                        position: 'bottom',
                        text: 'Humidity, %',
                    }
                },
            });

            this.moisture_chart = new Chart(this.moisture, {
                type: 'doughnut',
                data: {
                    labels: ['Moisture', 'Max'],
                    datasets: [{
                        data: [0, 100],
                        backgroundColor: [
                            'rgba(153, 102, 255, 1)',
                            'rgba(153, 102, 255, .2)'
                        ]
                    }]
                },
                options: {
                    title: {
                        display: true,
                        position: 'bottom',
                        text: 'Moisture, %'
                    }
                },
            });

            this.update();

            setInterval(
                () => this.update(),
                5 * 60 * 1000
            );
        }

        update() {
            $.getJSON('/api?limit=1', (data) => {
                this.temp_chart.data.datasets[0].data = [
                    data['temp'][0], 100 - data['temp'][0]
                ];
                this.temp_chart.update();

                this.humidity_chart.data.datasets[0].data = [
                    data['humidity'][0], 100 - data['humidity'][0]
                ];
                this.humidity_chart.update();

                this.moisture_chart.data.datasets[0].data = [
                    data['moisture'][0], 100 - data['moisture'][0]
                ];
                this.moisture_chart.update();
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
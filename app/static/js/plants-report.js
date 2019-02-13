(($) => {

    'use strict';

    class PlantsReportWidget {
        constructor() {
            this.status = $('#status');
            this.chart = $('#plants-report');

            this.options = {
                responsive: true,
                legend: {
                    position: 'bottom',
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                },
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Date'
                        }
                    }],
                    yAxes: [{
                        name: 'A',
                        position: 'left',
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Temperature'
                        }
                    }, {
                        name: 'B',
                        position: 'right',
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Humidity / Moisture'
                        }
                    }]
                }
            };

            this.scales = {
                A: {
                    absolute: {
                        min: 0,
                        max: 100
                    },
                    stacked: {
                        min: 15,
                        max: 85
                    }
                },
                B: {
                    absolute: {
                        min: 0,
                        max: 100
                    },
                    stacked: {
                        min: 15,
                        max: 85
                    }
                }
            };
        }

        init() {
            this.chart = new Chart(this.chart, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        index: 'temp',
                        label: 'Temperature, C',
                        fill: false,
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgb(255, 99, 132)',
                        data: [],
                        yAxesGroup: 'A'
                    }, {
                        index: 'humidity',
                        label: 'Humidity, %',
                        fill: false,
                        borderColor: 'rgba(54, 162, 235)',
                        backgroundColor: 'rgba(54, 162, 235)',
                        data: [],
                        yAxesGroup: 'B'
                    }, {
                        index: 'moisture',
                        label: 'Moisture, %',
                        fill: false,
                        borderColor: 'rgb(153, 102, 255)',
                        backgroundColor: 'rgb(153, 102, 255)',
                        data: [],
                        yAxesGroup: 'B'
                    }]
                },
                options: this.options,
            });

            this.update();

            setInterval(
                () => this.update(),
                5 * 60 * 1000
            );

            $('#limit, #group, .type').on(
                'change',
                () => this.update()
            );
        }

        update() {
            let limit = $('#limit').val(),
                group = $('#group').val(),
                type = $('.type:checked').val();

            $.getJSON('/api?limit=' + limit + '&group=' + group, (data) => {
                this.chart.data.labels = data['label'];

                this.chart.data.datasets.forEach((dataset) => {
                    dataset.data = data[dataset.index];
                });

                this.chart.options.scales.yAxes.forEach((value) => {
                    value.ticks = {
                        min: this.scales[value.name][type]['min'],
                        max: this.scales[value.name][type]['max'],
                        stepSize: 10
                    };
                });

                this.chart.update();
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

    $.plants_report = new PlantsReportWidget();

})(jQuery);
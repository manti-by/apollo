(($) => {

    'use strict';

    let $status = $('#status'),
        $chart = $('#line-chart'),
        options = {
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
        },
        scales = {
            A: {
                absolute: {
                    min: 0,
                    max: 100
                },
                stacked: {
                    min: 15,
                    max: 35
                }
            },
            B: {
                absolute: {
                    min: 0,
                    max: 100
                },
                stacked: {
                    min: 55,
                    max: 85
                }
            }
        };

    // Init default chart mode
    options.scales.yAxes.forEach((value) => {
        value.min = scales[value.name][OPTIONS['type']]['min'];
        value.max = scales[value.name][OPTIONS['type']]['max'];
    });


    // Setup line chart
    let chart = new Chart($chart, {
        type: 'line',
        data: {
            labels: DATA['label'],
            datasets: [{
                index: 'temp',
                label: "Temperature, C",
                fill: false,
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgb(255, 99, 132)',
                data: DATA['temp'],
                yAxesGroup: 'A'
            }, {
                index: 'humidity',
                label: "Humidity, %",
                fill: false,
                borderColor: 'rgba(54, 162, 235)',
                backgroundColor: 'rgba(54, 162, 235)',
                data: DATA['humidity'],
                yAxesGroup: 'B'
            }, {
                index: 'moisture',
                label: "Moisture, %",
                fill: false,
                borderColor: 'rgb(153, 102, 255)',
                backgroundColor: 'rgb(153, 102, 255)',
                data: DATA['moisture'],
                yAxesGroup: 'B'
            }]
        },
        options: options,
    });


    // Periodically update chart from server
    let update_chart = () => {
        $.getJSON('/api' + window.location.search, (data) => {
            chart.data.labels = data['label'];

            chart.data.datasets.forEach((dataset) => {
                dataset.data = data[dataset.index];
            });

            chart.update();
        }).done(() => {
            let now = new Date();
            $status
                .removeClass('text-danger')
                .addClass('text-secondary')
                .text(
                    'Last update: ' + now.getHours() + ':' + now.getMinutes()
                );
        }).fail(() => {
            $status
                .removeClass('text-secondary')
                .addClass('text-danger')
                .text('Connection error');
        });
    };

    setInterval(update_chart, 5 * 60 * 1000);

    // Listen controls
    $('select.limit, select.group').on('change', update_chart);

    $('input.type').on('change', (event) => {
        let type = $(event.currentTarget).val();

        chart.options.scales.yAxes.forEach((value) => {
            value.min = scales[value.name][type]['min'];
            value.max = scales[value.name][type]['max'];
        });

        chart.update();
    });

})(jQuery);
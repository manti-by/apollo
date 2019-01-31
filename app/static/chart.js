(($) => {

    'use strict';

    let $chart = $("#chart"),
        $msg = $("#message");

    let chart = new Chart($chart, {
        type: 'line',
        data: {
            labels: DATA_SET['label'],
            datasets: [{
                index: 'temp',
                label: "Temperature, C",
                fill: false,
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgb(255, 99, 132)',
                data: DATA_SET['temp'],
            }, {
                index: 'humidity',
                label: "Humidity, %",
                fill: false,
                borderColor: 'rgba(54, 162, 235)',
                backgroundColor: 'rgba(54, 162, 235)',
                data: DATA_SET['humidity'],
            }, {
                index: 'moisture',
                label: "Moisture, %",
                fill: false,
                borderColor: 'rgb(153, 102, 255)',
                backgroundColor: 'rgb(153, 102, 255)',
                data: DATA_SET['moisture'],
            }]
        },
        options: {
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
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                }]
            }
        },
    });

    setInterval(() => {
        $.getJSON('/api', (data) => {
            $msg.addClass('d-none');

            chart.data.labels = data['label'];

            chart.data.datasets.forEach((dataset) => {
                dataset.data = data[dataset.index];
            });

            chart.update();
        }).fail(() => {
            $msg.removeClass('d-none')
                .text('Failed to fetch data from server');
        });
    }, 10000);

})(jQuery);
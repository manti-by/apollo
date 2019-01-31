(($) => {

    'use strict';

    let $chart = $("#chart");

    let chart = new Chart($chart, {
        type: 'line',
        data: {
            labels: DATA_SET['label'],
            datasets: [{
                label: "Temperature, C",
                fill: false,
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgb(255, 99, 132)',
                data: DATA_SET['temp'],
            }, {
                label: "Humidity, %",
                fill: false,
                borderColor: 'rgba(54, 162, 235)',
                backgroundColor: 'rgba(54, 162, 235)',
                data: DATA_SET['humidity'],
            }, {
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

})(jQuery);
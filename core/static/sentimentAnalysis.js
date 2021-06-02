const canvas = document.getElementById('canvas1');
var ctx = canvas.getContext('2d');
Chart.defaults.plugins.legend.display = false;

const labels = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
];
const data = {
  labels: labels,
  datasets: [{
    label: 'My First Dataset',
    data: [65, 59, 80, 81, 56, 55, 40],
    fill: false,
    borderColor: 'rgb(75, 192, 192)',
    tension: 0.1
  }]
};
const options = {
  maintainAspectRatio: false,
  scales: {
    y: {
      grid: {
        color: 'white',
        borderColor: 'grey',
      },
      ticks: {
        color: "white", // this here
      },
    },
    x: {
      grid: {
        color: 'white',
        borderColor: 'grey',
      },
      ticks: {
        color: "white", // this here
      },
    }
  },
};
const config = {
  type: 'line',
  data: data,
  options: options
};
var myChart = new Chart(ctx, config);
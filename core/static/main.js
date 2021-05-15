const mapIframe = document.getElementById('map-iframe');
const btn1 = document.getElementById('btn1');
const btn2 = document.getElementById('btn2');
const btn3 = document.getElementById('btn3');
const btn4 = document.getElementById('btn4');
const btn5 = document.getElementById('btn5');

const maps = ['./map1.html', './map2.html', './map3.html', './map4.html', './map5.html']
btn1.addEventListener('click', (event) => {
  mapIframe.src = maps[0];
});
btn2.addEventListener('click', (event) => {
  mapIframe.src = maps[1];
});

fetch('http://127.0.0.1:5000/api/getroutes', {
  method: 'GET',
  mode:'cors'
}).then(response => {
  console.log(response);
  return response.json();
}).then(data => {
  console.log('received data in json');
  console.log(data);
  return data;
});
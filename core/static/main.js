import data from './routesSampleResponse.js';
const cityLinkBtn = document.getElementById('city-link-btn');
const posLajuBtn = document.getElementById('pos-laju-btn');
const gdexBtn = document.getElementById('gdex-btn');
const jAndTBtn = document.getElementById('j-and-t-btn');
const dhlBtn = document.getElementById('dhl-btn');
const btns = [cityLinkBtn, posLajuBtn, gdexBtn, jAndTBtn, dhlBtn];
const map_canvas_cityLinkExpress = document.getElementById('map_canvas_cityLinkExpress');
const map_canvas_posLaju = document.getElementById('map_canvas_posLaju');
const map_canvas_gdex = document.getElementById('map_canvas_gdex');
const map_canvas_jnt = document.getElementById('map_canvas_jnt');
const map_canvas_dhl = document.getElementById('map_canvas_dhl');
const canvas = [map_canvas_cityLinkExpress
  , map_canvas_posLaju
  , map_canvas_gdex, map_canvas_jnt, map_canvas_dhl
]
const hubInfo = [
  {
    title: 'City-link Express',
    deliveryHub: 'Port Klang',
    coordinate: `3.0319924887507144, \n101.37344116244806`
  },
  {
    title: 'Pos Laju',
    deliveryHub: 'Petaling Jaya',
    coordinate: `3.112924170027219, \n101.63982650389863 `
  },
  {
    title: 'GDEX',
    deliveryHub: 'Batu Caves',
    coordinate: `3.265154613796736, \n101.68024844550233`
  },
  {
    title: 'J&T',
    deliveryHub: 'Kajang',
    coordinate: `2.9441205329488325, \n101.7901521759029 `
  },
  {
    title: 'DHL',
    deliveryHub: 'Sungai Buloh',
    coordinate: `3.2127230893650065, \n101.57467295692778`
  },
]

btns.forEach((btn, idx) => {
  console.log(btn);
  btn.addEventListener('click', (event) => {
    displayNone(event.currentTarget.id);
    event.preventDefault();
    // mapIframe.setAttribute('src', maps[idx]);
    // deactive the active element
    const cur = document.getElementsByClassName('active');
    cur[0].className = cur[0].className.replace(' active', '');
    btn.classList.add('active');
  });
});

function displayNone(btnId) {
  document.getElementsByClassName('custom-d-none')[0].classList.remove("custom-d-none");
  switch (btnId) {
    case "city-link-btn": {
      canvas[0].classList.toggle("custom-d-none");
      break;
    }
    case "pos-laju-btn": {
      canvas[1].classList.toggle("custom-d-none");
      break;
    }
    case "gdex-btn": {
      canvas[2].classList.toggle("custom-d-none");
      break;
    }
    case "j-and-t-btn": {
      canvas[3].classList.toggle("custom-d-none");
      break;
    }
    case "dhl-btn": {
      canvas[4].classList.toggle("custom-d-none");
      break;
    }
  }
}
function error(input, message) {
  input.classList.add('error');
  // show the error message
  const error = input.previousElementSibling;
  error.innerText = message;
  return false;
}
function success(input) {
  input.classList.add('success');
  // hide the error message
  const error = input.previousElementSibling;
  error.innerText = '';
  return true;
}
function requireValue(input, message) {
  return input.value.trim() === '' ?
    error(input, message) :
    success(input);
}
const form = document.getElementById('generate-maps');
let startEle = form.elements['start-destination'];
let endEle = form.elements['end-destination'];
const requiredFields = [
  { input: startEle, message: 'Start destination is required' },
  { input: endEle, message: 'End destination is required' }
];
function initialize(mapCanvasEle, originLat, originLng, hubLat, hubLng, destinationLat, destinationLng, legs) {
  var map = new google.maps.Map(mapCanvasEle, {
    zoom: 3,
    center: new google.maps.LatLng(hubLat, hubLng)
  });
  // parse legs
  let hubIdx = -1, minLat = 100, minLng = 100;
  legs.forEach((leg, index) => {
    console.log(leg.start[0] + " " + leg.start[1]);
    console.log(hubLat + " " + hubLng);
    if (Math.abs(leg.start[0] - hubLat) <= minLat && Math.abs(leg.start[1] - hubLng) <= minLng) {
      minLat = Math.abs(leg.start[0] - hubLat);
      minLng = Math.abs(leg.start[1] - hubLng);
      hubIdx = index;
      console.log('found');
    }
  });
  console.log(hubIdx);
  const legsAfterHub = legs.splice(hubIdx);
  console.log(legs);
  console.log(legsAfterHub);
  const googleLatLngLegsArr = legs.map(leg => {
    return google.maps.geometry.encoding.decodePath(leg.polyline.points);
  });
  const googleLatLngLegsArr2 = legsAfterHub.map(leg => {
    return google.maps.geometry.encoding.decodePath(leg.polyline.points);
  });
  const googleLatLngLegsBeforeHub = [];
  const googleLatLngLegsAfterHub = [];
  googleLatLngLegsArr.forEach(arr => { arr.forEach(pt => googleLatLngLegsBeforeHub.push(pt)); });
  googleLatLngLegsArr2.forEach(arr => { arr.forEach(pt => googleLatLngLegsAfterHub.push(pt)); });

  new google.maps.Polyline({
    clickable: false,
    geodesic: true,
    strokeColor: "#6495ED",
    strokeOpacity: 1.000000,
    strokeWeight: 3,
    map: map,
    path: [
      new google.maps.LatLng(originLat, originLng),
      ...googleLatLngLegsBeforeHub
    ]
  });
  new google.maps.Polyline({
    clickable: false,
    geodesic: true,
    strokeColor: "#fb0",
    strokeOpacity: 1.000000,
    strokeWeight: 3,
    map: map,
    path: [
      // new google.maps.LatLng(originLat, originLng),
      ...googleLatLngLegsAfterHub
    ]
  });

  var origin = new google.maps.LatLng(originLat, originLng);
  var hub = new google.maps.LatLng(hubLat, hubLng);
  var destination = new google.maps.LatLng(destinationLat, destinationLng);

  var marker = new google.maps.Marker({
    position: origin,
    map: map
  });
  var marker = new google.maps.Marker({
    position: hub,
    map: map
  });
  var marker = new google.maps.Marker({
    position: destination,
    map: map
  });

  var bounds = new google.maps.LatLngBounds();
  bounds.extend(origin);
  bounds.extend(hub);
  bounds.extend(destination);
  map.fitBounds(bounds);
  return map;
}

form.addEventListener('submit', evt => {
  console.log('form submitted, initialise all map on canvas.');
  evt.preventDefault();
  let start = startEle.value;
  let end = endEle.value;
  // check required fields
  let valid = true;
  requiredFields.forEach((input) => {
    valid = requireValue(input.input, input.message);
  });
  const requestData = {
    start: start,
    end: end
  };
  if (valid) {
    // comment below block if not calling /getroutes
    fetch('http://127.0.0.1:5000/api/getroutes', {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData),
    }).then(response => {
      return response.json();
    }).then(data => {
      console.log(data);
      // rearrange the route to in correct order within the array
      const cityInfo = data.routes.filter(route => route.hub === 'City-link Express')[0];
      const posInfo = data.routes.filter(route => route.hub === 'Pos Laju')[0];
      const gdexInfo = data.routes.filter(route => route.hub === 'GDEX')[0];
      const jntInfo = data.routes.filter(route => route.hub === 'J&T')[0];
      const dhlInfo = data.routes.filter(route => route.hub === 'DHL')[0];
      const couriers = [cityInfo, posInfo, gdexInfo, jntInfo, dhlInfo];
      // console.log(couriers);
      // console.log(JSON.stringify(data));
      canvas.forEach((single_canvas, index) => {
        // console.log(single_canvas);
        // const courier = data.routes[index];
        const courier = couriers[index];
        const { origin, hubLocation, destination } = courier;
        console.log(courier);
        initialize(single_canvas, origin[0], origin[1], hubLocation[0], hubLocation[1], destination[0], destination[1], courier.legs);
        console.log('push map index ' + index);
      });
      displayNone('city-link-btn');

      // update result table
      console.log('hi');
      const resultTableTbody = document.getElementById('result-table-tbody');
      // console.log(resultTableTbody);
      const tbodyChildNode = resultTableTbody.querySelectorAll('tr');
      // console.log(tbodyChildNode);
      tbodyChildNode.forEach((row, index) => {
        const tableDataArr = Array.from(row.querySelectorAll('td'));
        // console.log(tableDataArr);
        const tempHub = hubInfo.filter(hub => hub.title === data.routes[index]['hub'])[0];
        tableDataArr[0].innerText = tempHub.title;
        tableDataArr[1].innerText = tempHub.deliveryHub;
        tableDataArr[2].innerText = tempHub.coordinate;
        const distance = parseFloat(data.routes[index]['distance']);
        tableDataArr[3].innerText = distance.toFixed(2);
      })
      // comment below block if not calling /getroutes
      return data;
    });
  }
});
console.log('Load analysis');
fetch('http://127.0.0.1:5000/api/getAnalysis', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
}).then(response => {
  return response.json();
}).then(data => {
  const ret = data.result;
  console.log(ret);
  function insertAfter(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
  }
  const chartTitle = document.getElementById('chart-title');
  // get max for chart
  // show whether the courier company is positive or negative
  const getResult = (value) => {
    if (value === 1) return "Positive";
    else if (value === -1) return "Negative";
    else return "Neutral";
  };
  // use this data to render charts in html
  const titles = ['City-link Express', 'Pos Laju', 'GDEX', 'J&T', 'DHL'];
  ret.reverse().forEach((article, index) => {
    const { negative, neutral, positive } = article.frequency;
    const div = document.createElement('div');
    div.setAttribute('class', 'px-4 pb-5 col-12 col-lg-8');
    div.setAttribute('style', 'height: 15rem;');
    div.innerHTML = `
    <div id="title_${index}"></div>
    <canvas id="myChart_${index}"></canvas>`;
    var ctx = div.querySelector(`#myChart_${index}`).getContext('2d');
    Chart.defaults.plugins.legend.display = false;
    var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Negative', 'Neutral', 'Positive'],
        datasets: [{
          // label: ['My','s', 't'],
          label: "Number of word",
          color: "white",
          data: [negative, neutral, positive],
          backgroundColor: [
            'rgba(54, 162, 235, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(54, 162, 235, 1)',
          ],
        }]
      },
      options: {
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
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
        indexAxis: 'y',
      }
    });
    // get max length out of all bars
    const values = Object.keys(article.frequency).map(key => article.frequency[key]);
    const cap = div.querySelector(`#title_${index}`);
    cap.setAttribute('class', 'mt-2');
    cap.innerHTML = article.title + ` - <i>${getResult(article.result_value)} article</i>`;
    insertAfter(div, chartTitle);
    // insert courier company name
    if ((index - 2) % 3 === 0) {
      const tempH6 = document.createElement('h4');
      tempH6.setAttribute('class', 'text-white col-12 pl-4 pt-4 d-flex justify-content-center');
      tempH6.innerText = titles[titles.length - 1];
      titles.pop();
      insertAfter(tempH6, chartTitle);
    }
  });
});

// direct to analysis page
const directBtn = document.getElementById('direct-to-analysis-page');
directBtn.addEventListener('click', () => {
  window.location.href = window.location.href + "/sentimentAnalysis.html";
});
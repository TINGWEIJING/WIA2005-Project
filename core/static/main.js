// http://127.0.0.1:5000/api/getAnalysis
const mapIframe = document.getElementById('map-iframe');
const cityLinkBtn = document.getElementById('city-link-btn');
const posLajuBtn = document.getElementById('pos-laju-btn');
const gdexBtn = document.getElementById('gdex-btn');
const jAndTBtn = document.getElementById('j-and-t-btn');
const dhlBtn = document.getElementById('dhl-btn');
const btns = [cityLinkBtn, posLajuBtn, gdexBtn, jAndTBtn, dhlBtn];
const maps = ['cityLinkMap.html', 'posLajuMap.html', 'gdexMap.html', 'jAndTMap.html', 'dhlMap.html'];
btns.forEach((btn, idx) => {
  console.log(btn);
  btn.addEventListener('click', (event) => {
    event.preventDefault();
    mapIframe.setAttribute('src', maps[idx]);
    // deactive the active element
    const cur = document.getElementsByClassName('active');
    cur[0].className = cur[0].className.replace(' active', '');
    btn.classList.add('active');
  });
});

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
form.addEventListener('submit', evt => {
  console.log('form submitted');
  evt.preventDefault();
  let start = startEle.value;
  let end = endEle.value;
  // check required fields
  let valid = true;
  requiredFields.forEach((input) => {
    valid = requireValue(input.input, input.message);
  });
  const data = {
    start: start,
    end: end
  };
  if (valid) {
    fetch('http://127.0.0.1:5000/api/getroutes', {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data),
    }).then(response => {
      return response.json();
    }).then(data => {
      console.log(data);
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
  const getMax = (a, b) => Math.max(a, b);
  const constructOneBar = (value, maxLen, row) => {
    const td = document.createElement('td');
    const span1 = document.createElement('span');
    span1.setAttribute('class', 'data');
    const span2 = document.createElement('span');
    span2.setAttribute('class', 'tooltip');
    span2.innerText = value;
    td.setAttribute('style', `--size: calc( ${value}/${maxLen} )`);
    td.appendChild(span1);
    td.appendChild(span2);
    // td.innerText = value;
    row.appendChild(td);
  }
  // show whether the courier company is positive or negative
  const getResult = (value) => {
    if (value === 1) return "Positive";
    else if (value === -1) return "Negative";
    else return "Neutral";
  };
  // use this data to render charts in html
  const titles = ['City-link Express', 'Pos Laju', 'GDEX', 'J&T', 'DHL'];
  ret.reverse().forEach((article,index) => {
    
    const div = document.createElement('div');
    div.setAttribute('class', 'px-4 py-2 col-12 col-lg-8');
    div.setAttribute('style', 'height: 15rem;');
    div.innerHTML = `
    <table class="charts-css bar datasets-spacing-5 show-primary-axis  multiple show-heading">
      <caption class="text-white h6"><a href=${article.url} class="text-primary"> ${article.title} </a></caption>
      <tbody>
          <tr id="chart-row">
              <th scope="row"> ${article.courier} </th>
          </tr>
      </tbody>
    </table>`;
    const chartRow = div.querySelector('#chart-row');
    // get max length out of all bars
    const values = Object.keys(article.frequency).map(key => article.frequency[key]);
    let maxLen = values.reduce(getMax);
    values.forEach(value => {
      constructOneBar(value, maxLen, chartRow);
    });
    const cap = chartRow.parentElement.previousElementSibling;
    cap.innerHTML += ` - <i>${getResult(article.result_value)} article</i>`;
    insertAfter(div, chartTitle);
    // insert courier company name
    if((index-2)%3 === 0){
      const tempH6 = document.createElement('h4');
      tempH6.setAttribute('class', 'text-white col-12 pl-4 pt-4');
      tempH6.innerText = titles[titles.length-1];
      titles.pop();
      insertAfter(tempH6, chartTitle);
    }
  });
});

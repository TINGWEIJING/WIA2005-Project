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
  // use this data to render charts in html
  const cityLinkRow = document.getElementById('city-link-row');
  const posLajuRow = document.getElementById('pos-laju-row');
  const gdexRow = document.getElementById('gdex-row');
  const jAndTRow = document.getElementById('j-and-t-row');
  const dhlRow = document.getElementById('dhl-row');
  const reducer = (acc, cur) => {
    const negative = acc.negative + cur.negative;
    const neutral = acc.neutral + cur.neutral;
    const positive = acc.positive + cur.positive;
    const ret = {
      negative: negative,
      neutral: neutral,
      positive: positive
    }
    return ret;
  }
  // calculate
  const cityFreq = ret.filter(dt => dt.courier === "City-link Express").map(ele => { return { ...ele.frequency }; });
  const posFreq = ret.filter(dt => dt.courier === "Pos Laju").map(ele => ele.frequency);
  const gdexFreq = ret.filter(dt => dt.courier === "GDEX").map(ele => ele.frequency);
  const jAndTFreq = ret.filter(dt => dt.courier === "J&T").map(ele => ele.frequency);
  const dhlFreq = ret.filter(dt => dt.courier === "DHL").map(ele => ele.frequency);
  const cityStat = cityFreq.reduce(reducer);
  const posStat = posFreq.reduce(reducer);
  const gdexStat = gdexFreq.reduce(reducer);
  const jAndTStat = jAndTFreq.reduce(reducer);
  const dhlStat = dhlFreq.reduce(reducer);
  // get max for chart
  const getMax = (a, b) => Math.max(a,b);
  const tempArr = [cityStat, posStat, gdexStat, jAndTStat, dhlStat];
  // let maxLen = 0;
  let maxLen = tempArr.reduce((acc, cur) => {
    return getMax(acc,Object.keys(cur).map(key => cur[key]).reduce(getMax))
  },0);
  console.log(maxLen);
  // start constructing
  const constructOneCompanyChart = (value, row) => {
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
  Object.keys(cityStat).map(key => cityStat[key]).forEach(value => constructOneCompanyChart(value, cityLinkRow));
  Object.keys(posStat).map(key => posStat[key]).forEach(value => constructOneCompanyChart(value, posLajuRow));
  Object.keys(gdexStat).map(key => gdexStat[key]).forEach(value => constructOneCompanyChart(value, gdexRow));
  Object.keys(jAndTStat).map(key => jAndTStat[key]).forEach(value => constructOneCompanyChart(value, jAndTRow));
  Object.keys(dhlStat).map(key => dhlStat[key]).forEach(value => constructOneCompanyChart(value, dhlRow));
  // show whether the courier company is positive or negative
  const getResult = (arr) => {
    const pos = arr.positive;
    const neg = arr.negative;
    const neu = arr.neutral;
    if(pos>=neg && pos>=neu) return "Positive";
    else if(neg>=pos && neg>=neu) return "Negative";
    else return "Neutral";
  };
  const cityCap = cityLinkRow.parentElement.previousElementSibling;
  cityCap.innerHTML += ` - <i>${getResult(cityStat)} article</i>`; 
  const posCap = posLajuRow.parentElement.previousElementSibling;
  posCap.innerHTML += ` - <i>${getResult(posStat)} article</i>`; 
  const gdexCap = gdexRow.parentElement.previousElementSibling;
  gdexCap.innerHTML += ` - <i>${getResult(gdexStat)} article</i>`; 
  const jAndTCap = jAndTRow.parentElement.previousElementSibling;
  jAndTCap.innerHTML += ` - <i>${getResult(jAndTStat)} article</i>`; 
  const dhlCap = dhlRow.parentElement.previousElementSibling;
  dhlCap.innerHTML += ` - <i>${getResult(dhlStat)} article</i>`; 
});

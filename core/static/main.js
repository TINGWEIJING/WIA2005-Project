// http://127.0.0.1:5000/api/getAnalysis
const mapIframe = document.getElementById('map-iframe');

const maps = ['./map1.html', './map2.html', './map3.html', './map4.html', './map5.html'];

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
  console.log(start);
  console.log(end);
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
        // 'Content-Type': 'application/x-www-form-urlencoded',
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

// call api to get audio
fetch('http://127.0.0.1:5000/api/getAudio', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
}).then(response => {
  return response.json();
}).then(data => {
  // console.log(data);
  const { full_target_audio, sample_audio_1, sample_audio_2 } = data;
  const targetAudioEle = document.getElementById('target-audio');
  const sourceArr = Array.from(targetAudioEle.querySelectorAll('source'));
  sourceArr.forEach(srcEle => {
    srcEle.setAttribute('src', full_target_audio.target_audio_path);
  });
  const youtubeLink = document.getElementById('youtube-link');
  youtubeLink.setAttribute('href', full_target_audio.source_link);
  // transcript
  const transcript = document.getElementById('transcript');
  transcript.innerText = full_target_audio.transcript;
  // table
  const sample1Table = document.getElementById('result-sample-1-table-tbody');
  const sample2Table = document.getElementById('result-sample-2-table-tbody');
  const buildTable = (sample_audio, tableHTML) => {
    sample_audio.forEach(word => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
      <td class="w-100 audio-graph-height">
        <img src='${word.graph_img_path}' alt="" class="graph-img-height">
      </td>
      <td><audio controls>
          <source src="${word.actual_audio_path}" type="audio/ogg">
          <source src="${word.actual_audio_path}" type="audio/mpeg">
          Your browser does not support the audio element.
        </audio>
        <div class="col-12 d-flex justify-content-center pt-1 h4">${word.actual_word}</div></td>
      <td><audio controls>
          <source src="${word.detected_audio_path}" type="audio/ogg">
          <source src="${word.detected_audio_path}" type="audio/mpeg">
          Your browser does not support the audio element.
        </audio>
      </td>
      `;
      tableHTML.appendChild(tr);
    });
  }
  buildTable(sample_audio_1, sample1Table);
  buildTable(sample_audio_2, sample2Table);
});
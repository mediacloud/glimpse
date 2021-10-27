
function submitSearch() {
  fetchAndRender('/api/count-over-time.json', 'results-count-over-time', renderCountOverTime);
  fetchAndRender('/api/count.json', 'results-count',
    (destinationId, data) => document.getElementById(destinationId).innerHTML = `<h2>Total Matching</h2><p>${data}</p>`
  );
  fetchAndRender('/api/sample.json', 'results-sample', renderSample);
}

function getSearchParams(){
  return {
    platform: document.getElementById("platform").value,
    terms: document.getElementById("terms").value,
    startDate: document.getElementById("startDate").value,
    endDate: document.getElementById("endDate").value
  }
}

function fetchAndRender(url, destinationId, renderer) {
  document.getElementById(destinationId).innerHTML = "Loading...";
  fetch(url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(getSearchParams())
      })
    .then(response => response.json())
    .then(data => {
      document.getElementById(destinationId).innerHTML = "";
      renderer(destinationId, data)
    });
}

function renderCountOverTime(destinationId, data) {
  vl.markLine()
    .width(1100)
    .data(data['counts'])
    .encode(
      vl.x().fieldT('date'),
      vl.y().fieldQ('count'),
      vl.tooltip('count')
    )
    .render()
    .then(viewElement => {
      // render returns a promise to a DOM element containing the chart
      // viewElement.value contains the Vega View object instance
      const h2Element = document.createElement("h2");
      const textNode = document.createTextNode("Matching Over Time");
      h2Element.appendChild(textNode);
      const destinationElement = document.getElementById(destinationId);
      destinationElement.appendChild(h2Element);
      destinationElement.appendChild(viewElement);
    });
}

function renderSample(destinationId, data) {
  var tableContent = `
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Date</th>
          <th scope="col">Author</th>
          <th scope="col">Content</th>
          <th scope="col">Source</th>
        </tr>
      </thead>
  `;
  const rows = data.map(d => `
    <tr>
      <td>${d['publish_date']}</td>
      <td>${d['author']}</td>
      <td>${d['content']}</td>
      <td><a href="${d['url']}">${d['media_name']}</a></td>
    </tr>
  `);
  for(idx in rows){
    tableContent += row[idx];
  }
  tableContent += "</table>";

  document.getElementById(destinationId).innerHTML = `
    <h2>Sample Content</h2>
    ${tableContent}
  `;
}

function dataToTableHTML(tableBodyId, data) {
  // https://stackoverflow.com/questions/17684201/create-html-table-from-javascript-object/17684427
  const tbody = "";
  for (var i = 0; i < obj.length; i++) {
    var tr = "<tr>";
    tr += "<td>" + obj[i].key + "</td>" + "<td>$" + obj[i].value.toString() + "</td></tr>";
    /* We add the table row to the table body */
    tbody += tr;
  }
  return tbody;
}

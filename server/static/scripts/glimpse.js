
function _getSearchParams(){
  return {
    platform: document.getElementById("platform").value,
    terms: document.getElementById("terms").value,
    startDate: document.getElementById("startDate").value,
    endDate: document.getElementById("endDate").value
  }
}

function submitSearch() {
  document.getElementById('count-over-time').innerHTML = "Loading...";
  fetch('/api/count-over-time.json', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(_getSearchParams())
      })
    .then(response => response.json())
    .then(data => renderCountOverTime(data));
}

function renderCountOverTime(data) {
  document.getElementById('count-over-time').innerHTML = "";
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
      document.getElementById('count-over-time').appendChild(viewElement);
    });
}

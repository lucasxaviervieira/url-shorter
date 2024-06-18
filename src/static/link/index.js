async function getUrl(url_id) {
  await fetch(`http://127.0.0.1:5000/api/url/${url_id}`, {
    method: 'GET',
  }
  )
    .then(response => response.json())
    .then(data => { showUrlShorted(data.shorter_url) });
}
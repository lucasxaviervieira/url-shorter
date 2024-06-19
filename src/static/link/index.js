async function getUrl(url_id) {
  await fetch(`http://127.0.0.1:5000/api/url/${url_id}`, {
    method: 'GET',
  }
  )
    .then(response => response.json())
    .then(data => { window.location.href = (data.original_url) });
}

function getLinkId() {
  const linkId = document.getElementById('link-id').textContent
  getUrl(linkId)
}

getLinkId()

async function createUrl(original_url) {
  await fetch('http://127.0.0.1:5000/api/url/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      original_url
    })

  }
  )
    .then(response => response.json())
    .then(data => { showUrlShorted(data.shorter_url) });
}

function showUrlShorted(shortUrl) {
  const newUrl = document.getElementById('new-url')
  newUrl.innerText = shortUrl
  newUrl.classList.remove('opacity-0')
}


function shortUrl() {
  const form = document.getElementById('url-form')
  form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const url = document.getElementById('original-url').value;

    await createUrl(url)

  });
}

shortUrl()
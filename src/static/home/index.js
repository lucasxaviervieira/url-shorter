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
  newUrl.href = shortUrl
  newUrl.innerText = shortUrl
  const div = newUrl.parentNode
  div.classList.remove('cursor-default', 'opacity-0')

  const copyButton = document.getElementById('copy-button');

  copyButton.addEventListener('click', function () {
    const tempInput = document.createElement('input');
    tempInput.value = shortUrl;
    document.body.appendChild(tempInput);


    tempInput.select();
    tempInput.setSelectionRange(0, 99999); // For mobile devices

    document.execCommand('copy');

    document.body.removeChild(tempInput);

    alert('Link copied to clipboard: ' + shortUrl);
  });

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
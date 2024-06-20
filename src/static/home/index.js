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
    .then(data => { verifyResponse(data) });
}

function verifyResponse(responseData) {
  const messageError = responseData.message
  const urlExists = 'This URL exists'
  const noHttps = 'This not longer an URL'

  switch (messageError) {
    case urlExists:
      alert('URL existe')
      break;
    case noHttps:
      alert('Não é uma URL')
      break;
    default:
      showUrlShorted(responseData)
  }
}

function showUrlShorted(data) {
  const originalUrl = data.original_url
  const shortUrl = data.shorter_url
  const qrCode = data.svg_qrcode
  const newUrl = document.getElementById('new-url')
  newUrl.href = shortUrl
  newUrl.innerText = shortUrl
  const div = newUrl.parentNode
  div.classList.remove('cursor-default', 'opacity-0')
  showCopyLinkButton(originalUrl)
  showQRCode(qrCode)
}

function showCopyLinkButton(originalUrl) {
  const copyButton = document.getElementById('copy-button');

  copyButton.addEventListener('click', function () {
    const tempInput = document.createElement('input');
    tempInput.value = originalUrl;
    document.body.appendChild(tempInput);


    tempInput.select();
    tempInput.setSelectionRange(0, 99999); // For mobile devices

    document.execCommand('copy');

    document.body.removeChild(tempInput);

    alert('Link copied to clipboard: ' + originalUrl);
  });
}

function showQRCode(qrCode) {
  const qrCodeElement = document.getElementById('qr-code')
  qrCodeElement.innerHTML = qrCode
  qrCodeElement.classList.remove('hidden')
}

function startShorter() {
  const form = document.getElementById('url-form')
  form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const url = document.getElementById('original-url').value;

    await createUrl(url)

  });
}

startShorter()
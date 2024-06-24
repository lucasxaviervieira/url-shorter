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
  const noHttps = 'This not longer an URL'
  const urlExists = 'This URL exists'

  switch (messageError) {
    case noHttps:
      alert(noHttps)
      break;
    case urlExists:
      alert(urlExists)
      showUrlShorted(responseData.data)
      break;
    default:
      showUrlShorted(responseData)
  }
}

function showUrlShorted(data) {
  const originalUrl = data.original_url
  const shortUrl = data.shorter_url
  const qrCode = data.svg_qrcode

  const hiddenContent = document.getElementById('hidden-content')
  const newUrl = document.getElementById('new-url')

  newUrl.href = shortUrl
  newUrl.innerText = shortUrl

  showCopyLinkButton(originalUrl)
  showQRCode(qrCode)

  hiddenContent.classList.remove('hidden')
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
    
    const copied = document.getElementById('copy-ok')
    copied.classList.remove('hidden')
  });
}

function showQRCode(qrCode) {
  const qrCodeElement = document.getElementById('qr-code')
  qrCodeElement.innerHTML = qrCode
}

function startShorter() {
  const form = document.getElementById('url-form')
  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    
    const copied = document.getElementById('copy-ok')
    copied.classList.add('hidden')

    const url = document.getElementById('original-url').value;

    await createUrl(url)

  });
}

startShorter()
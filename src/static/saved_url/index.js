async function getUrl() {
  await fetch(`http://127.0.0.1:5000/api/url/`, {
    method: 'GET',
  }
  )
    .then(response => response.json())
    .then(data => {
      showSaved(data)
    });
}

function createElement(data) {
  const newDiv = document.createElement('div')


  newDiv.classList.add('flex', 'flex-col', 'gap-y-3', 'justify-center', 'items-center');


  const originalUrl = document.createElement('p')
  const shorter_url = document.createElement('p')
  const svgQRCode = document.createElement('span')

  originalUrl.innerText = data.original_url
  shorter_url.innerText = data.shorter_url
  svgQRCode.innerHTML = data.svg_qrcode


  newDiv.appendChild(originalUrl)
  newDiv.appendChild(shorter_url)
  newDiv.appendChild(svgQRCode)
  return newDiv
}

function showSaved(data) {
  const savedUrlContainer = document.getElementById('saved-url')

  data.forEach(el => {
    console.log(el)
    const newDiv = createElement(el)
    savedUrlContainer.appendChild(newDiv)
  });

}

async function startSavedUrl() {

  await getUrl()
}

startSavedUrl()
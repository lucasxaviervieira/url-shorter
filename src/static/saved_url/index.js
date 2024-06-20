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

function createContent(data, whatsEl) {
  const url = document.createElement('div')
  const title = document.createElement('p')
  const content = document.createElement('span')
  
  const originalUrl = 'original_url'
  const shorterUrl = 'shorter_url'
  const svgQRCode = 'svg_qrcode'
  
  switch (whatsEl) {
    case originalUrl: {
      title.innerText = "original url"
      content.innerText = data.original_url
      break
    }
    case shorterUrl: {
      title.innerText = "shorter url"
      content.innerText = data.shorter_url
      break
    }
    case svgQRCode: {
      title.innerText = "QR Code"
      // content.innerHTML = data.svg_qrcode
      content.innerHTML = '<div style="display: block; width: 75px; height: 75px; background-color: #ccc; border: 1px solid #666; margin: 0 auto;"></div>'

    }
  }

  url.appendChild(title)
  url.appendChild(content)
  return url
}


function createElement(data) {
  const newDiv = document.createElement('div')

  newDiv.classList.add('flex', 'flex-col', 'gap-y-3', 'justify-center', 'items-center');

  const originalUrl = createContent(data, 'original_url')
  const shorterUrl = createContent(data, 'shorter_url')
  const svgQRCode = createContent(data, 'svg_qrcode')


  newDiv.appendChild(originalUrl)
  newDiv.appendChild(shorterUrl)
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
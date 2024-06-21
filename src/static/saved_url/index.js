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
  const content = document.createElement('div')
  
  const originalUrl = 'original_url'
  const shorterUrl = 'shorter_url'
  const svgQRCode = 'svg_qrcode'
  
  switch (whatsEl) {
    case originalUrl: {
      title.innerText = "Original URL:"
      content.innerText = data.original_url
      content.classList.add('text-blue-500', 'hover:text-blue-800', 'select-all');
      break
    }
    case shorterUrl: {
      title.innerText = "Shorted URL:"
      const shortedLink = document.createElement('p')
      shortedLink.innerText = data.shorter_url
      shortedLink.id = data.id
      const copyButton = createCopyLinkButton(data.shorter_url)      
      
      content.classList.add('flex', 'items-center', 'gap-x-1');
      content.classList.add('text-blue-500');
      
      content.appendChild(shortedLink)
      content.appendChild(copyButton)
      break
    }
    case svgQRCode: {
      title.innerText = "QR Code:"
      const span = document.createElement('span')
      span.innerHTML = data.svg_qrcode

      const svgElement = span.querySelector('svg');

      svgElement.setAttribute('width', '144');
      svgElement.setAttribute('height', '144');       

      content.appendChild(span)
      content.classList.add('max-h-36', 'max-w-36')
      // content.innerHTML = '<div style="display: block; width: 144px; height: 144px; background-color: #ccc; border: 1px solid #666; margin: 0 auto;"></div>'
    }
  }

  url.appendChild(title)
  url.appendChild(content)
  url.classList.add('text-center', 'overflow-hidden', 'max-w-48', 'lg:max-w-56', '2xl:max-w-96')  
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
    const newDiv = createElement(el)
    savedUrlContainer.appendChild(newDiv)
  });

}

function createCopyLinkButton(link) {
  const copyButton = document.createElement('button')
  copyButton.innerHTML = '<svg width="20px" height="20px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 7H16C18.7614 7 21 9.23858 21 12C21 14.7614 18.7614 17 16 17H14M10 7H8C5.23858 7 3 9.23858 3 12C3 14.7614 5.23858 17 8 17H10M8 12H16" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

  const shortedUrl = link
  

  copyButton.addEventListener('click', function () {
    const tempInput = document.createElement('input');
    tempInput.value = shortedUrl;
    document.body.appendChild(tempInput);


    tempInput.select();
    tempInput.setSelectionRange(0, 99999); // For mobile devices

    document.execCommand('copy');

    document.body.removeChild(tempInput);

    alert('Link copied to clipboard: ' + shortedUrl);
  })
  return copyButton
  ;
}

async function startSavedUrl() {
  
  await getUrl()
}

startSavedUrl()
import qrcode
import qrcode.image.svg

from io import BytesIO


def generate_qr_code_with_expiry(url, expiration_date):
    url_with_expiry = f"{url}?expiry={expiration_date.strftime('%Y-%m-%d')}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        image_factory=qrcode.image.svg.SvgPathImage,
    )

    qr.add_data(url_with_expiry)
    qr.make(fit=True)

    svg_bytes = BytesIO()

    qr.make_image(image_factory=qrcode.image.svg.SvgPathImage).save(svg_bytes)

    svg_bytes.seek(0)

    svg_string = svg_bytes.read().decode("utf-8")

    return svg_string

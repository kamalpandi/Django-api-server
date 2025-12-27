from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

# Precomputed ASCII characters from darkest to lightest
ASCII_CHARS = ["@", "#", "S", "%", "? ", "*", "+", ";", ":", ",", ". "]


def convert_image_to_ascii(image_file, width=80):
    """
    Optimized ASCII art converter for low-resource environments
    """
    try:
        # Open image with minimal memory footprint
        img = Image.open(image_file)

        # 1. REDUCE IMAGE SIZE FIRST (biggest CPU saver)
        img = img.convert('RGB')
        aspect_ratio = img.height / img.width
        new_height = int(width * aspect_ratio * 0.55)
        img = img.resize((width, new_height), Image.Resampling.BILINEAR)

        # 2. USE NUMPY FOR FASTER PIXEL PROCESSING (if available)
        try:
            import numpy as np
            pixels = np.array(img)

            # Vectorized brightness calculation
            brightness = (
                                 pixels[:, :, 0] * 0.299 +  # R
                                 pixels[:, :, 1] * 0.587 +  # G
                                 pixels[:, :, 2] * 0.114  # B
                         ) / 255

            ascii_indices = (brightness * (len(ASCII_CHARS) - 1)).astype(int)

            ascii_art = []
            for y in range(ascii_indices.shape[0]):
                row_html = []
                for x in range(ascii_indices.shape[1]):
                    char = ASCII_CHARS[ascii_indices[y, x]]
                    r, g, b = int(pixels[y, x, 0]), int(pixels[y, x, 1]), int(pixels[y, x, 2])
                    row_html.append(f'<span style="color: rgb({r},{g},{b})">{char}</span>')
                ascii_art.append("".join(row_html))

            return "<br>".join(ascii_art)

        except ImportError:
            # Fallback for no NumPy - still optimized
            pixels = list(img.getdata())
            width_px = img.width

            ascii_art = []
            for i, pixel in enumerate(pixels):
                if i % width_px == 0:
                    ascii_art.append("<br>")

                r, g, b = pixel
                # Standard luminance formula (faster than sum)
                brightness = int((r * 0.299 + g * 0.587 + b * 0.114) / 255 * (len(ASCII_CHARS) - 1))
                char = ASCII_CHARS[brightness]

                ascii_art.append(f'<span style="color:rgb({r},{g},{b})">{char}</span>')

            return "".join(ascii_art)

    except Exception as e:
        return f"<p style='color:  red;'>Error: {str(e)}</p>"


@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "POST":
        if not request.FILES.get('image'):
            return HttpResponse("No image file found in request!", status=400)
        image_file = request.FILES['image']
        # Use smaller default width for free tier
        width = int(request.POST.get('width', 70))
        width = max(40, min(width, 120))  # Reduced max from 200 to 120

        ascii_html = convert_image_to_ascii(image_file, width)

        if request.headers.get('HX-Request'):
            return HttpResponse(f'''
                <pre style="font-family: monospace; font-size: 7px; line-height: 1; 
                            background: #000; color: #0f0; padding: 10px; 
                            overflow:  auto; max-height: 600px;">
                    {ascii_html}
                </pre>
            ''')

        return render(request, 'index.html', {'ascii_result': ascii_html})

    return render(request, 'pic_to_ASCII/index.html')

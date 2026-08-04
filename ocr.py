import urllib.request
import urllib.parse
import json
import base64
import sys
import os

def ocr_image(filepath):
    url = "https://api.ocr.space/parse/image"
    with open(filepath, "rb") as f:
        image_data = f.read()
    encoded = base64.b64encode(image_data).decode("utf-8")
    data = urllib.parse.urlencode({
        "base64Image": f"data:image/png;base64,{encoded}",
        "language": "spa",
        "isOverlayRequired": "false",
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    req.add_header("apikey", "helloworld")
    req.add_header("User-Agent", "Mozilla/5.0")
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        result = json.loads(resp.read().decode("utf-8"))
        if result.get("IsErroredOnProcessing"):
            return f"ERROR: {result.get('ErrorMessage')}"
        parsed_text = result.get("ParsedResults")[0]["ParsedText"] if result.get("ParsedResults") else ""
        return parsed_text.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"

if __name__ == "__main__":
    files = [
        "vuelo.png", "coche.png", "edimburgo.png",
        "glasgos.png", "inverness.png", "skye.png", "balloch.png",
        "castillo-edimburgo.png", "Castillo Urquhart Reserva.png",
        "Reserva Lago Ness.png", "Reserva Lago Ness precio.png",
        "reserva-coche-castillourquhart.png"
    ]
    for fname in files:
        fpath = os.path.join(os.path.dirname(__file__), "Booking", fname)
        if os.path.exists(fpath):
            print(f"\n{'='*60}")
            print(f"=== {fname} ===")
            print(f"{'='*60}")
            text = ocr_image(fpath)
            print(text)
        else:
            print(f"\n=== {fname} - NOT FOUND ===")

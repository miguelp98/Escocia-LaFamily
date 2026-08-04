import zlib
import re

with open("/home/migue/viajes/Scotland/Booking/Crucero por el lago Ness y el canal de Caledonia Inverness - Booking.com.pdf", "rb") as f:
    data = f.read()

# Quick scan - find stream boundaries more efficiently
pattern = re.compile(rb'stream\s(.+?)\nendstream', re.DOTALL)
matches = list(pattern.finditer(data))
print(f"Found {len(matches)} streams")

for idx, m in enumerate(matches):
    raw = m.group(1).strip()
    # Skip very large streams (images)
    if len(raw) > 100000:
        print(f"Stream {idx+1}: SKIPPED (image, {len(raw)} bytes)")
        continue
    try:
        decompressed = zlib.decompress(raw)
        try:
            text = decompressed.decode("utf-8", errors="replace")
            # Extract text between parentheses in PDF operators
            texts = re.findall(r'\(([^)]*)\)', text)
            if texts:
                clean = ' '.join(t.strip() for t in texts if len(t.strip()) > 1)
                if clean:
                    print(f"\n=== Stream {idx+1} ===")
                    print(clean[:3000])
        except:
            pass
    except:
        print(f"Stream {idx+1}: not compressed or not text")

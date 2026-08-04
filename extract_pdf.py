import zlib
import re

with open("/home/migue/viajes/Scotland/Booking/Crucero por el lago Ness y el canal de Caledonia Inverness - Booking.com.pdf", "rb") as f:
    data = f.read()

# Find all stream objects and try to decompress
streams = []
i = 0
while True:
    stream_start = data.find(b"stream\n", i)
    if stream_start == -1:
        stream_start = data.find(b"stream ", i)
    if stream_start == -1:
        break
    stream_start = data.find(b"\n", stream_start) + 1
    
    stream_end = data.find(b"\nendstream", stream_start)
    if stream_end == -1:
        stream_end = data.find(b"endstream", stream_start)
    if stream_end == -1:
        break
    
    raw = data[stream_start:stream_end]
    try:
        decompressed = zlib.decompress(raw)
        try:
            text = decompressed.decode("utf-8", errors="replace")
            if re.search(r'[A-Za-z]{3,}', text):
                streams.append(text)
        except:
            pass
    except:
        pass
    
    i = stream_end + 9

print(f"Found {len(streams)} text streams")
for idx, s in enumerate(streams):
    print(f"\n{'='*60}")
    print(f"=== Stream {idx+1} ===")
    print(f"{'='*60}")
    # Clean up and show readable text
    text = s
    # Remove PDF operators
    text = re.sub(r'\(([^)]*)\)\s*Tj', r'\1', text)
    text = re.sub(r'\(([^)]*)\)\s*TJ', r'\1', text)
    text = re.sub(r'\[(.*?)\]\s*TJ', lambda m: ''.join(re.findall(r'\(([^)]*)\)', m.group(1))), text)
    text = re.sub(r'ET.*?BT', ' ', text, flags=re.DOTALL)
    text = re.sub(r'[^\x20-\x7E\n\xC0-\xFF]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    print(text[:2000])

import urllib.request, json, re

def test_video(vid):
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read().decode())
        return data.get('title')
    except Exception as e:
        return None

# Search for widescreen 16:9 official This Old House or Home Depot P-Trap video
queries = [
    "How to Replace a PVC Sink Trap This Old House",
    "How to Fix a Leaking Sink Drain Pipe Home Depot",
    "How to Install a P-Trap Lowes"
]

for q in queries:
    search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}"
    req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        found_ids = list(dict.fromkeys(re.findall(r'/watch\?v=([a-zA-Z0-9_-]{11})', html)))
        print(f"Query: {q}")
        for vid in found_ids[:6]:
            title = test_video(vid)
            if title:
                print(f"  >>> ID: {vid} | Title: {title}")
    except Exception as e:
        print(f"Error: {e}")

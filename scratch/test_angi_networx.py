import urllib.request

urls = [
    "https://www.angi.com/nearme/plumbing/",
    "https://www.angi.com/nearme/handyman/",
    "https://www.angi.com/nearme/drywall-repair/",
    "https://www.networx.com/c.plumbing",
    "https://www.networx.com/c.handyman",
    "https://www.networx.com/c.drywall",
    "https://www.networx.com/c.water-heaters"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

for u in urls:
    req = urllib.request.Request(u, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        print(f"PASS [{resp.getcode()}]: {u}")
    except Exception as e:
        print(f"FAIL: {u} -> {e}")

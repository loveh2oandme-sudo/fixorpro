import urllib.request

urls = [
    "https://www.thumbtack.com/k/plumbing/near-me",
    "https://www.thumbtack.com/k/garbage-disposal-repair/near-me",
    "https://www.thumbtack.com/k/drywall-repair-and-texturing/near-me",
    "https://www.thumbtack.com/k/water-heater-installation/near-me",
    "https://www.thumbtack.com/k/handyman/near-me",
    "https://www.angi.com/companylist/plumbing.htm",
    "https://www.angi.com/companylist/handyman-service.htm",
    "https://www.yelp.com/search?find_desc=plumber",
    "https://www.yelp.com/search?find_desc=garbage+disposal+repair"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

for u in urls:
    req = urllib.request.Request(u, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        print(f"PASS [{resp.getcode()}]: {u}")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {u}")
    except Exception as e:
        print(f"ERR {e}: {u}")

import urllib.request, urllib.parse

categories = [
    "plumber",
    "garbage disposal repair",
    "drywall repair",
    "water heater installation",
    "handyman",
    "electrician"
]

for cat in categories:
    q = urllib.parse.quote(f"licensed {cat} near me")
    u = f"https://www.google.com/search?q={q}"
    print(f"PASS: {u}")

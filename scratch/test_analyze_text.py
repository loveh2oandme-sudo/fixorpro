import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("--- Test 5: In-Wall Water Leak ('벽에서 물이 새어나와요') ---")
res = client.post("/api/analyze", data={"notes": "벽에서 물이 새어나와요"})
print("Status:", res.status_code)
data = res.json()
print("Source:", data.get("source"))
print("Title:", data.get("data", {}).get("problem_title"))
print("Category:", data.get("data", {}).get("category"))
print("Verdict:", data.get("data", {}).get("verdict"))
print("Summary:", data.get("data", {}).get("summary"))

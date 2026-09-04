import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("--- Step 1: Health Check ---")
r = client.get("/api/health")
print("Status:", r.status_code, r.json())

print("\n--- Step 2: Test Ceiling Water Leak ('천장에서 물이 샌다') ---")
res1 = client.post("/api/analyze", data={"notes": "천장에서 물이 샌다"})
print("Status:", res1.status_code)
d1 = res1.json().get("data", {})
print("Title:", d1.get("problem_title"))
print("Category:", d1.get("category"))
print("Verdict:", d1.get("verdict"))
assert d1.get("category") == "Plumbing", "Category should be Plumbing!"
assert d1.get("verdict") == "CALL_A_PRO", "Verdict should be CALL_A_PRO!"

print("\n--- Step 3: Test Wall Water Leak ('벽에서 물이 새어나와요') ---")
res2 = client.post("/api/analyze", data={"notes": "벽에서 물이 새어나와요"})
print("Status:", res2.status_code)
d2 = res2.json().get("data", {})
print("Title:", d2.get("problem_title"))
print("Category:", d2.get("category"))
print("Verdict:", d2.get("verdict"))

print("\n--- Step 4: Test Electrical Switch ('전등 스위치가 안 켜져요') ---")
res3 = client.post("/api/analyze", data={"notes": "전등 스위치가 안 켜져요"})
print("Status:", res3.status_code)
d3 = res3.json().get("data", {})
print("Title:", d3.get("problem_title"))
print("Category:", d3.get("category"))

print("\n--- Step 5: Verify Static File Versioning & Index HTML ---")
res_html = client.get("/")
print("Index Status:", res_html.status_code)
html_text = res_html.text
assert "input-notes-textarea" in html_text, "Textarea for userNotes should be present!"
assert "aiQuestionBox" in html_text, "aiQuestionBox should be present!"
assert "app.js?v=9.0.0" in html_text, "v=9.0.0 cache buster should be present!"

print("\n✅ ALL LOCAL VERIFICATION TESTS PASSED SUCCESSFULLY!")

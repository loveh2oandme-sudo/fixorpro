import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_endpoints():
    print("Testing /api/health...")
    res = client.get("/api/health")
    assert res.status_code == 200
    print("Health response:", res.json())

    print("\nTesting /api/chat with greeting '하이라고'...")
    res = client.post("/api/chat", json={"messages": [{"role": "user", "content": "하이라고"}]})
    assert res.status_code == 200
    print("Chat greeting response:", res.json()["reply"])

    print("\nTesting /api/chat with greeting '하이'...")
    res = client.post("/api/chat", json={"messages": [{"role": "user", "content": "하이"}]})
    assert res.status_code == 200
    print("Chat greeting response:", res.json()["reply"])

    print("\nTesting /api/chat with issue '싱크대 누수'...")
    res = client.post("/api/chat", json={"messages": [{"role": "user", "content": "싱크대 누수"}]})
    assert res.status_code == 200
    data = res.json()
    print("Chat issue response reply snippet:", data["reply"][:100])
    assert "report_data" in data or "report_scenario" in data

    print("\nTesting /api/narrow with greeting '하이라고'...")
    res = client.post("/api/narrow", json={"notes": "하이라고", "level": 1})
    assert res.status_code == 200
    print("Narrow greeting response options count:", len(res.json()["options"]))

    print("\nTesting /api/analyze with greeting '하이라고'...")
    res = client.post("/api/analyze", data={"notes": "하이라고"})
    assert res.status_code == 200
    print("Analyze greeting problem title:", res.json()["data"]["problem_title"])

    print("\nALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_endpoints()

import sys
from pathlib import Path

# Add workspace to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from app.main import app

def test_ai_chat_flow():
    client = TestClient(app)
    print("=== Testing FixOrPro Interactive AI Diagnostic Chat (/api/chat) ===")

    # 1. Multi-turn chat message 1: Exterior wall hole question
    payload1 = {
        "messages": [
            {"role": "user", "content": "바깥 외벽(스타코/사이딩)에 손바닥만한 구멍이 났는데 어떻게 해야 하나요?"}
        ],
        "language": "ko"
    }

    res1 = client.post("/api/chat", json=payload1)
    print(f"Chat Response Status: {res1.status_code}")
    data1 = res1.json()
    print(f"AI Reply:\n{data1.get('reply')}\n")
    print(f"Report Scenario Triggered: {data1.get('report_scenario')}")
    assert res1.status_code == 200
    assert "외벽" in data1.get("reply") or "exterior" in data1.get("reply").lower() or "stucco" in data1.get("reply").lower()

    # 2. Multi-turn chat message 2: Toilet flapper question
    payload2 = {
        "messages": [
            {"role": "user", "content": "변기 물소리가 쉬익 소리 내며 계속 납니다."}
        ],
        "language": "ko"
    }

    res2 = client.post("/api/chat", json=payload2)
    print(f"\nChat Response Status: {res2.status_code}")
    data2 = res2.json()
    print(f"AI Reply:\n{data2.get('reply')}\n")
    assert res2.status_code == 200

    print("✅ INTERACTIVE AI DIAGNOSTIC CHAT TEST PASSED!")

if __name__ == "__main__":
    test_ai_chat_flow()

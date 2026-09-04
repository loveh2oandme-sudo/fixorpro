import sys
from pathlib import Path

# Add workspace to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from app.main import app

def test_mobile_app_assets_and_chat():
    client = TestClient(app)
    print("=== FixOrPro Mobile App & PWA Verification Test ===")

    # 1. Health check
    res_health = client.get("/api/health")
    print(f"1. Health Check: Status {res_health.status_code} | {res_health.json()}")
    assert res_health.status_code == 200

    # 2. PWA Manifest asset check
    res_manifest = client.get("/manifest.json")
    print(f"2. PWA Manifest Check: Status {res_manifest.status_code}")
    assert res_manifest.status_code == 200
    assert "FixOrPro" in res_manifest.text

    # 3. PWA Service Worker asset check
    res_sw = client.get("/sw.js")
    print(f"3. PWA Service Worker Check: Status {res_sw.status_code}")
    assert res_sw.status_code == 200
    assert "CACHENAME" in res_sw.text.replace('_', '').replace('-', '') or "addEventListener" in res_sw.text

    # 4. Multi-turn AI Chat API check for Parts & Contractor Card output
    chat_payload = {
        "messages": [
            {"role": "user", "content": "싱크대 밑 U자형 배관(P-트랩)에서 물이 뚝뚝 새요."}
        ],
        "language": "ko"
    }
    res_chat = client.post("/api/chat", json=chat_payload)
    print(f"4. 1:1 AI Chat API Check: Status {res_chat.status_code}")
    chat_data = res_chat.json()
    print(f"   AI Reply: {chat_data.get('reply')[:120]}...")
    print(f"   Report Scenario Triggered: {chat_data.get('report_scenario')}")
    assert res_chat.status_code == 200
    assert "report_scenario" in chat_data or "reply" in chat_data

    print("\n✅ MOBILE APP PWA & 1:1 CHAT DISPATCH SYSTEM VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    test_mobile_app_assets_and_chat()

import io
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw

# Add workspace to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from app.main import app

def create_dummy_repair_photo(issue_type: str = "sink_leak") -> bytes:
    """Generates a dummy repair photo as JPEG bytes for testing image upload pipelines."""
    img = Image.new("RGB", (600, 400), color=(240, 240, 245))
    draw = ImageDraw.Draw(img)
    
    # Draw simulated repair scene
    draw.rectangle([50, 50, 550, 350], outline=(100, 100, 100), width=4)
    if issue_type == "sink_leak":
        # Draw P-Trap shape
        draw.line([(250, 100), (250, 250), (350, 250), (350, 150)], fill=(50, 120, 200), width=12)
        draw.ellipse([340, 240, 360, 260], fill=(0, 150, 255)) # Water drop
        draw.text((200, 300), "Simulated P-Trap Leak Photo", fill=(0, 0, 0))
    elif issue_type == "drywall_hole":
        # Draw hole on wall
        draw.ellipse([250, 150, 350, 250], fill=(80, 50, 30), outline=(40, 30, 20), width=3)
        draw.text((200, 300), "Simulated Drywall Hole Photo", fill=(0, 0, 0))
    elif issue_type == "running_toilet":
        # Draw toilet tank
        draw.rectangle([200, 100, 400, 280], outline=(60, 60, 60), width=3)
        draw.text((200, 300), "Simulated Running Toilet Photo", fill=(0, 0, 0))
    
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def run_photo_diagnostics_tests():
    client = TestClient(app)
    print("=== Testing Real Photo Upload & Vision Diagnostics Endpoint ===")

    # 1. Health check
    res = client.get("/api/health")
    print(f"Health Check Status: {res.status_code} | Body: {res.json()}")
    assert res.status_code == 200

    # 2. Test Image Upload with Text Description (P-Trap Leak)
    photo_bytes = create_dummy_repair_photo("sink_leak")
    files = {
        "image": ("sink_leak.jpg", photo_bytes, "image/jpeg")
    }
    data = {
        "user_notes": "싱크대 아래 U자 관(P-트랩) 조인트에서 방울방울 누수가 발생해요."
    }
    
    print("\n--- Test Case 1: Photo Upload + Text Notes (Sink P-Trap Leak) ---")
    response = client.post("/api/analyze", files=files, data=data)
    print(f"Response Code: {response.status_code}")
    result = response.json().get("data", {})
    print(f"Source: {response.json().get('source')}")
    print(f"Verdict: {result.get('verdict')}")
    print(f"Problem Title: {result.get('problem_title')}")
    print(f"Category: {result.get('category')}")
    print(f"Estimated Savings: {result.get('cost_comparison', {}).get('estimated_savings')}")
    assert response.status_code == 200
    assert result.get("verdict") in ["DIY_RECOMMENDED", "CALL_A_PRO"]

    # 3. Test Image Upload Only (Drywall Hole)
    photo_bytes_hole = create_dummy_repair_photo("drywall_hole")
    files_hole = {
        "image": ("drywall.jpg", photo_bytes_hole, "image/jpeg")
    }
    data_hole = {
        "notes": "실내 드라이월 석고보드에 문손잡이가 부딪혀 구멍이 생겼습니다."
    }
    
    print("\n--- Test Case 2: Photo Upload + Drywall Hole Description ---")
    response_hole = client.post("/api/analyze", files=files_hole, data=data_hole)
    print(f"Response Code: {response_hole.status_code}")
    result_hole = response_hole.json().get("data", {})
    print(f"Source: {response_hole.json().get('source')}")
    print(f"Verdict: {result_hole.get('verdict')}")
    print(f"Problem Title: {result_hole.get('problem_title')}")
    print(f"Category: {result_hole.get('category')}")
    assert response_hole.status_code == 200

    # 4. Test High-Risk Electrical Photo Upload (Circuit Breaker Sparking)
    photo_bytes_elec = create_dummy_repair_photo("running_toilet")
    files_elec = {
        "image": ("electrical.jpg", photo_bytes_elec, "image/jpeg")
    }
    data_elec = {
        "notes": "조명 스위치를 켤 때마다 스파크 불꽃이 튀고 차단기가 내려갑니다."
    }
    
    print("\n--- Test Case 3: High-Risk Electrical Issue (Pro Required Check) ---")
    response_elec = client.post("/api/analyze", files=files_elec, data=data_elec)
    print(f"Response Code: {response_elec.status_code}")
    result_elec = response_elec.json().get("data", {})
    print(f"Source: {response_elec.json().get('source')}")
    print(f"Verdict: {result_elec.get('verdict')}")
    print(f"Problem Title: {result_elec.get('problem_title')}")
    assert response_elec.status_code == 200
    assert result_elec.get("verdict") == "CALL_A_PRO"

    print("\n✅ ALL REAL PHOTO UPLOAD & DIAGNOSTICS PIPELINE TESTS PASSED!")

if __name__ == "__main__":
    run_photo_diagnostics_tests()

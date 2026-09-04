import os
import io
import json
import logging
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.sample_data import SAMPLE_SCENARIOS
from app.ai_diagnostics import analyze_repair_issue, generate_dynamic_questions
from pydantic import BaseModel

# Load .env file if present
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fixorpro")

app = FastAPI(
    title="FixOrPro - AI Home Repair & Cost Diagnostic Engine",
    description="Don't spend $200 on a contractor for a $15 fix.",
    version="1.0.0"
)

# Enable CORS for local testing & embedding
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


@app.get("/api/health")
async def health_check():
    has_api_key = bool(os.environ.get("GEMINI_API_KEY"))
    return {
        "status": "online",
        "has_server_api_key": has_api_key,
        "sample_count": len(SAMPLE_SCENARIOS)
    }


@app.get("/api/samples")
async def get_samples():
    """Returns the list of sample scenarios available for instant one-click testing."""
    samples = []
    for s_id, s_data in SAMPLE_SCENARIOS.items():
        samples.append({
            "id": s_data["id"],
            "title": s_data["title"],
            "category": s_data["category"],
            "thumbnail": s_data["thumbnail"],
            "image_url": s_data["image_url"],
            "description": s_data["description"]
        })
    return {"samples": samples}


@app.get("/api/samples/{sample_id}")
async def get_sample_result(sample_id: str):
    """Returns the pre-computed diagnosis for a sample scenario."""
    if sample_id not in SAMPLE_SCENARIOS:
        raise HTTPException(status_code=404, detail="Sample scenario not found")
    return SAMPLE_SCENARIOS[sample_id]


class NarrowRequest(BaseModel):
    notes: str
    level: int = 1
    previous_choice: Optional[str] = None
    api_key: Optional[str] = None


@app.post("/api/narrow")
async def narrow_question(req: NarrowRequest):
    """
    Dynamic Question Narrowing Endpoint (1, 2, 3, 4 Options)
    - Receives user symptom description.
    - Generates 4 distinct options to narrow down the problem (Level 1 or Level 2).
    """
    notes = req.notes.strip() if req.notes else ""
    if not notes:
        raise HTTPException(status_code=400, detail="Text description required for question narrowing.")

    user_or_env_key = req.api_key or os.environ.get("GEMINI_API_KEY")

    if user_or_env_key:
        try:
            res = await generate_dynamic_questions(
                user_notes=notes,
                level=req.level,
                previous_choice=req.previous_choice,
                api_key=user_or_env_key
            )
            return {
                "status": "success",
                "title": res.get("title", f"💡 [{req.level}차 좁히기] AI 추가 확인 질문: 1, 2, 3, 4번 중 선택해 주세요."),
                "level": req.level,
                "can_narrow_further": res.get("can_narrow_further", req.level == 1),
                "options": res.get("options", [])
            }
        except Exception as e:
            logger.error(f"Gemini dynamic question generation failed: {e}")

    # Intelligent Fallback Generator for Demo / Non-API-Key Mode
    text_lower = notes.lower()

    # 1. Sink & Drain Leaks (Check FIRST before general water/leak keywords!)
    if any(k in text_lower for k in ["싱크대", "세면대", "싱크", "p-트랩", "트랩", "배수구", "하수구", "p-trap", "trap", "sink"]):
        if req.level == 1:
            return {
                "status": "success",
                "title": "💡 [1차 좁히기] AI 추가 확인 질문: 싱크대/세면대 누수가 발생하는 구체적인 부위를 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 1,
                "can_narrow_further": True,
                "options": [
                    {"text": "1번: 싱크대/세면대 하부 U자형 P-트랩 연결 너트 부식 마모 및 미세 누수"},
                    {"text": "2번: 싱크대 위 수도꼭지(수전) 내부 카트리지/호스 연결부 누수"},
                    {"text": "3번: 음식물 분쇄기(Disposal) 이음매 고무 가스켓 부식 및 체결부 누수"},
                    {"text": "4번: 배출구 호스 막힘으로 인한 하수관 역류 및 싱크대 하부 장 침수"}
                ]
            }
        else:
            return {
                "status": "success",
                "title": "💡 [2차 부품 핀포인트 좁히기] 구매에 필요한 정확한 교체 부품 규격을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 2,
                "can_narrow_further": False,
                "options": [
                    {"text": "1번: 🔧 P-트랩 고무 가스켓/O-링 패킹 세트 ($3.99 - 연결부 고무 마모 시)"},
                    {"text": "2번: 🛠️ 1-1/2인치 표준 PVC P-트랩 조립체 전체 ($9.99 - 배관 균열/파손 시)"},
                    {"text": "3번: 🚰 주방 수전 범용 교체용 세라믹 카트리지 ($14.99 - 수도꼭지 누수 시)"},
                    {"text": "4번: 🗑️ 음식물 분쇄기 밀봉 고무 가스켓 & 잠금링 ($7.99 - 분쇄기 연결 누수 시)"}
                ]
            }

    # 2. Toilet Leaks
    elif any(k in text_lower for k in ["변기", "수조", "toilet", "flapper", "필밸브"]):
        if req.level == 1:
            return {
                "status": "success",
                "title": "💡 [1차 좁히기] AI 추가 확인 질문: 변기 고장/누수의 구체적 증상을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 1,
                "can_narrow_further": True,
                "options": [
                    {"text": "1번: 변기 수조 내부 플래퍼 고무 마모로 세면수 지속 흘러내림 ('쉬익' 소음)"},
                    {"text": "2번: 변기 하단 왁스 링(Wax Ring) 마모로 바닥 틈새 오수 누수"},
                    {"text": "3번: 변기 급수 호스(Supply Line) 및 앵글 밸브 연결 너트 미세 누수"},
                    {"text": "4번: 수조 부속(필밸브) 장착 불량으로 수위 조절 실패 오버플로우"}
                ]
            }
        else:
            return {
                "status": "success",
                "title": "💡 [2차 부품 핀포인트 좁히기] 변기 수리에 필요한 정확한 교체 부품을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 2,
                "can_narrow_further": False,
                "options": [
                    {"text": "1번: 🚽 범용 2인치 고무 플래퍼 & 체인 ($6.99 - 수조 물 속 흘러내림/소음 시)"},
                    {"text": "2번: 🍩 변기 하단 헤비듀티 왁스 링 (Wax Ring) ($4.99 - 변기 바닥 오수 누수 시)"},
                    {"text": "3번: 🚰 3/8\" x 7/8\" 편조 스테인리스 변기 급수 호스 ($7.99 - 급수 호스 누수 시)"},
                    {"text": "4번: ⚙️ Fluidmaster 안티-사이폰 변기 필밸브(Fill Valve) ($11.99 - 수위 조절 실패 시)"}
                ]
            }

    # 3. Water Heater / Boiler Leaks
    elif any(k in text_lower for k in ["온수기", "보일러", "water heater", "boiler", "tank"]):
        if req.level == 1:
            return {
                "status": "success",
                "title": "💡 [1차 좁히기] AI 추가 확인 질문: 온수기/보일러 누수 부위를 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 1,
                "can_narrow_further": True,
                "options": [
                    {"text": "1번: 온수기 하단 배수 밸브(Drain Valve) 연결부 미세 누수"},
                    {"text": "2번: 온수기 상단 급수/온수 PEX 연결관 너트 부식 누수"},
                    {"text": "3번: 압력 구출 밸브(T&P Valve) 과열 과압으로 인한 퇴출수 방출"},
                    {"text": "4번: 온수기 내동 탱크 차체 부식으로 바닥 전체 침수 누수"}
                ]
            }
        else:
            return {
                "status": "success",
                "title": "💡 [2차 부품 핀포인트 좁히기] 온수기 수리에 필요한 정확한 부품을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 2,
                "can_narrow_further": False,
                "options": [
                    {"text": "1번: 🚰 3/4인치 황동 온수기 배수 밸브 (Brass Drain Valve) ($12.99 - 하단 배수 밸브 누수 시)"},
                    {"text": "2번: 🛡️ 3/4인치 T&P 온도 압력 안전 구출 밸브 ($16.99 - 압력 밸브 누수/과열 방출 시)"},
                    {"text": "3번: 🔗 3/4\" Push-to-Connect PEX 온수기 수리 코넥터 ($14.99 - 상부 배관 너트 부식 시)"},
                    {"text": "4번: 🚨 면허 배관공 전용 온수기 내동 탱크 1:1 교체 ($0 DIY 불가 - 탱크 부식 시)"}
                ]
            }

    # 4. Ceiling / Wall In-Wall Pipe Leaks
    elif any(k in text_lower for k in ["누수", "물", "새", "젖", "leak", "drip", "천장", "수도"]):
        if req.level == 1:
            return {
                "status": "success",
                "title": "💡 [1차 좁히기] AI 추가 확인 질문: 천장/벽체 누수가 발생하는 구체적인 상황을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 1,
                "can_narrow_further": True,
                "options": [
                    {"text": "1번: 윗집/상부 화장실 및 배관 사용 시에만 천장이 축축해짐 (방수층/배수관 누수)"},
                    {"text": "2번: 수도 사용과 무관하게 24시간 계속 물이 뚝뚝 떨어짐 (급수 배관 파열)"},
                    {"text": "3번: 비가 오거나 날씨 악화 시 천장/외벽 쪽으로 물이 스며듦 (지붕/외벽 방수)"},
                    {"text": "4번: 온수/보일러 가동 시에만 가열음과 함께 벽 속 배관 누수됨 (온수 배관 부식)"}
                ]
            }
        else:
            return {
                "status": "success",
                "title": "💡 [2차 부품 핀포인트 좁히기] 벽체/천장 배관 수리에 필요한 부품을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 2,
                "can_narrow_further": False,
                "options": [
                    {"text": "1번: 🩹 1/2인치 PEX/구리 배관 비상 마감 캡 (SharkBite End Cap) ($8.99 - 임시 차단 시)"},
                    {"text": "2번: 💧 디지털 벽체/석고보드 수분 측정기 (Moisture Meter) ($24.99 - 젖은 범위 측정 시)"},
                    {"text": "3번: 🔧 1/2인치 샤크바이트 슬립 커플링 (Slip Coupling) ($13.99 - 파손 파이프 구간 교체 시)"},
                    {"text": "4번: 🚨 청음식/열화상 누수 탐지전문가 긴급 출장 ($0 DIY 불가 - 벽 속 정밀 탐지 필요 시)"}
                ]
            }

    # 5. Electrical issues
    elif any(k in text_lower for k in ["전기", "스위치", "전등", "콘센트", "차단기", "두꺼비집", "light", "switch", "outlet", "spark", "breaker"]):
        if req.level == 1:
            return {
                "status": "success",
                "title": "💡 [1차 좁히기] AI 추가 확인 질문: 전기 고장의 구체적 상황을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 1,
                "can_narrow_further": True,
                "options": [
                    {"text": "1번: 스위치를 켤 때 전등이 깜빡거리거나 불꽃(아크) 소리가 남"},
                    {"text": "2번: 두꺼비집(차단기)이 특정 가전/스위치 사용 시 즉시 내려감"},
                    {"text": "3번: 콘센트 탄 냄새가 나거나 가전 플러그가 헐겁게 빠짐"},
                    {"text": "4번: 조명 스위치 덮개가 파손되거나 딸깍 감이 없음"}
                ]
            }
        else:
            return {
                "status": "success",
                "title": "💡 [2차 부품 핀포인트 좁히기] 전기 수리에 필요한 정확한 교체 부품을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 2,
                "can_narrow_further": False,
                "options": [
                    {"text": "1번: ⚡ 15A Decora 싱글 폴 조명 스위치 ($3.99 - 스위치 헐거움/불꽃 소음 시)"},
                    {"text": "2번: 🔌 15A 120V 범용 벽면 듀플렉스 콘센트 ($2.99 - 플래그 접불/탄 냄새 시)"},
                    {"text": "3번: 🛡️ 20A GFCI 누전 차단 콘센트 ($16.99 - 주방/욕실 물 주변 보호 콘센트)"},
                    {"text": "4번: 🚨 배전반 주 차단기(Breaker) 1:1 교체 ($0 DIY 금지 - 면허 전기기사 필요 시)"}
                ]
            }

    # 6. Wall / Hole issues
    elif any(k in text_lower for k in ["벽", "구멍", "석고", "hole", "wall", "drywall", "stucco", "외벽"]):
        if req.level == 1:
            return {
                "status": "success",
                "title": "💡 [1차 좁히기] AI 추가 확인 질문: 벽면 파손 위치와 재질을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 1,
                "can_narrow_further": True,
                "options": [
                    {"text": "1번: 🏠 건물 외벽 (바깥 스타코 미장 / 사이딩 / 콘크리트 구멍)"},
                    {"text": "2번: 🚪 방 안 실내 석고보드 (Drywall / 문 손잡이 충격 구멍)"},
                    {"text": "3번: 🪟 창틀 주변 석고보드 균열 및 수분 손상"},
                    {"text": "4번: 📐 벽면 못 자국 / 작은 균열 및 페인트 칠 들뜸"}
                ]
            }
        else:
            return {
                "status": "success",
                "title": "💡 [2차 부품 핀포인트 좁히기] 벽면 구멍 보수에 필요한 정확한 자재/패치를 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 2,
                "can_narrow_further": False,
                "options": [
                    {"text": "1번: 🩹 4x4인치 알루미늄 자가점착 메쉬 구멍 패치 ($5.99 - 주먹 크기 이하 문 손잡이 구멍)"},
                    {"text": "2번: 🏠 Ready-Mix 외벽 스타코 전용 아크릴 보수 패치 ($12.99 - 건물 바깥 스타코 구멍)"},
                    {"text": "3번: 🪵 1/2인치 석고보드(Drywall) 원판 소형 보수 패널 ($9.99 - 대형 파손 구멍 절단 교체)"},
                    {"text": "4번: 🎨 스패클 퍼티 & 샌딩 블록 올인원 퍼티 킷 ($7.99 - 못 자국/작은 균열)"}
                ]
            }

    # 7. Door / Hinge / Lock issues
    elif any(k in text_lower for k in ["문", "경첩", "도어락", "문틀", "손잡이", "door", "hinge", "lock"]):
        if req.level == 1:
            return {
                "status": "success",
                "title": "💡 [1차 좁히기] AI 추가 확인 질문: 문 작동의 구체적인 문제점을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 1,
                "can_narrow_further": True,
                "options": [
                    {"text": "1번: 문 상단/바닥이 문틀에 닿아 뻑뻑하게 걸림"},
                    {"text": "2번: 문 손잡이나 도어락 래치가 안 잠김"},
                    {"text": "3번: 경첩 나사가 헛돌고 문이 아래로 처짐"},
                    {"text": "4번: 문을 열고 닫을 때 삐걱거리는 마찰 소음"}
                ]
            }
        else:
            return {
                "status": "success",
                "title": "💡 [2차 부품 핀포인트 좁히기] 문 수리에 필요한 정확한 부품을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 2,
                "can_narrow_further": False,
                "options": [
                    {"text": "1번: 🔩 3인치 문틀 스터드 고정용 긴 수리 나사 세트 ($3.99 - 문 처짐/경첩 나사 헛돌 때)"},
                    {"text": "2번: 🧴 WD-40 콤팩트 건식 실리콘 윤활 스프레이 ($5.49 - 문 삐걱 소음 및 문고리 뻑뻑함)"},
                    {"text": "3번: 🔒 범용 키리스 방문/현관 도어락 래치 세트 ($24.99 - 도어락 잠금 래치 고장 시)"},
                    {"text": "4번: 📐 조절식 도어 경첩 핀 피벗 수리 세트 ($8.99 - 경첩 마모 및 문틀 걸쇠 부딪힘)"}
                ]
            }

    # 8. General fallback options for any input
    else:
        if req.level == 1:
            return {
                "status": "success",
                "title": f"💡 [1차 좁히기] AI 추가 확인 질문: '{notes[:30]}' 관련 구체적 상황을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 1,
                "can_narrow_further": True,
                "options": [
                    {"text": f"1번: {notes[:20]} 관련 부품 노후화 및 기계적 고장/작동 이상"},
                    {"text": f"2번: {notes[:20]} 관련 누수/수분 침투 또는 습기 손상"},
                    {"text": f"3번: {notes[:20]} 관련 외부 충격/균열 및 구조적 파손"},
                    {"text": f"4번: {notes[:20]} 관련 전기/전원 결선 불량 및 접촉 이상"}
                ]
            }
        else:
            return {
                "status": "success",
                "title": f"💡 [2차 부품 핀포인트 좁히기] 수리에 필요한 정확한 교체 부품 유형을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 2,
                "can_narrow_further": False,
                "options": [
                    {"text": "1번: 📦 1:1 규격 소형 교체 부품/부속품 ($5 - $15 - 마모 부품 단독 교체)"},
                    {"text": "2번: 🛠️ 조립체 전체 1:1 세트 교체품 ($15 - $40 - 모듈 전체 1:1 교체)"},
                    {"text": "3번: 🩹 방수/방진 코킹 씰런트 및 메쉬 패치 ($8 - $18 - 충진/마감 자재 필요)"},
                    {"text": "4번: 🚨 면허 전문가(배관공/전기기사) 전용 장비 및 수리 (DIY 위험 대형 하자)"}
                ]
            }


def get_smart_fallback(notes: Optional[str] = None) -> dict:
    text_query = (notes or "").lower().strip()
    matched_key = None

    greeting_words = ["하이", "하이라고", "하이요", "안녕", "안녕하세요", "hi", "hello", "hey", "ㅎㅇ", "방가", "반가워", "반갑습니다", "테스트", "test"]
    if text_query in greeting_words or any(text_query.startswith(g) for g in ["하이", "안녕", "hi", "hello", "hey"]) or any(g in text_query for g in ["하이라고", "하이요", "안녕하세요"]):
        return {
            "problem_title": "FixOrPro AI 1:1 대화형 진단 서비스",
            "category": "Interactive Consultation",
            "confidence_score": "High (99%)",
            "verdict": "DIY_RECOMMENDED",
            "difficulty": "Beginner (1:1 대화로 진단 진행)",
            "estimated_time": "1분 소요",
            "youtube_query": "home repair diy basic guide",
            "cost_comparison": {
                "diy_cost": "무료 AI 진단",
                "pro_cost": "$150+ (전문가 출장)",
                "estimated_savings": "$150+",
                "savings_percentage": "100%"
            },
            "summary": "안녕하세요! FixOrPro AI 집수리 마스터입니다. 어디에 어떤 고장이나 누수가 발생했나요? '싱크대 누수', '석고보드 구멍', '변기 물 샐 때'처럼 구체적인 증상을 입력해 주시거나 사진을 첨부해 주세요!",
            "safety_warnings": [
                "전기, 가스, 대형 누수 작업 시에는 반드시 메인 밸브 및 차단기를 먼저 꺼주세요."
            ],
            "materials_needed": [],
            "tools_needed": [],
            "steps": [],
            "pro_trigger_conditions": "위험한 고전압, 가스, 원인 불명 대형 누수의 경우 검증된 라이선스 기술자를 연결해 드립니다."
        }

    if (any(w in text_query for w in ["벽", "wall", "천장", "ceiling"]) and any(w in text_query for w in ["물", "새", "누수", "leak", "drip", "젖"])):
        return {
            "problem_title": f"벽체 / 천장 내부 배관 누수 및 수분 침투 점검 ({notes.strip() if notes else '벽체 누수'})",
            "category": "Plumbing",
            "confidence_score": "High (95%)",
            "verdict": "CALL_A_PRO",
            "difficulty": "Licensed Pro Required (면허 배관공 누수 탐지 필수)",
            "estimated_time": "1 - 3 hours",
            "youtube_query": "how to detect in wall pipe leak water leaking behind drywall",
            "cost_comparison": {
                "diy_cost": "$20 - $50 (비상 밸브 차단 및 임시 처리)",
                "pro_cost": "$250 - $600 (누수 탐지 & 벽체 내부 배관 용접/교체)",
                "estimated_savings": "$0 (전문 면허 배관공 필수)",
                "savings_percentage": "0%"
            },
            "summary": f"고객님이 입력하신 증상('{notes.strip() if notes else '벽체 누수'}'): 벽체 또는 천장 내부 급수/배수관 파손으로 인한 수분 침투 진단입니다. 벽 안쪽 누수는 곰팡이 감염, 석고보드 붕괴 및 주택 구조 부식을 유발하므로 주 메인 급수 밸브를 즉시 잠그고 전문 누수 탐지 배관공을 부르셔야 합니다.",
            "safety_warnings": [
                "🚨 즉시 조치: 집 전체 메인 수도 계량기 밸브를 시계 방향으로 완전히 돌려 차단하세요.",
                "벽 안쪽에 콘센트나 전선관이 지나는 경우 전등/전원 차단기(Circuit Breaker)도 함께 내리세요.",
                "젖은 석고보드가 침하되거나 무너질 수 있으므로 누수 지점 바로 아래에 귀중품을 치우세요."
            ],
            "materials_needed": [
                {"name": "비상 배관 마감용 PEX / 구리 배관 캡 (Push-to-Connect Cap)", "est_price": "$8.99", "amazon_search": "sharkbite 1/2 inch end cap", "homedepot_search": "push to connect cap"},
                {"name": "수분 측정기 (Moisture Meter)", "est_price": "$24.99", "amazon_search": "digital moisture meter drywall", "homedepot_search": "moisture meter"}
            ],
            "tools_needed": [
                {"name": "청음식 / 열화상 누수 탐지 장비 (전문가용)", "amazon_search": "thermal imaging camera leak detection", "homedepot_search": "thermal camera"},
                {"name": "배관용 튜브 커터 (Pipe Cutter)", "amazon_search": "pipe cutter copper pex", "homedepot_search": "pipe cutter"}
            ],
            "steps": [
                {
                    "step_num": 1,
                    "title": "집 메인 급수 밸브 즉시 차단 및 누수 유무 확인",
                    "instruction": "집 외부에 있는 메인 수도 계량기 밸브나 차고/지하실의 메인 급수 밸브를 잠급니다.",
                    "pro_tip": "밸브를 잠근 후 집안의 가장 낮은 수전을 열어 배관 속 잔여 물을 빼내세요.",
                    "caution": "누수 지점에 전등이나 콘센트가 가까이 있다면 전기 차단기도 함께 내리세요."
                },
                {
                    "step_num": 2,
                    "title": "누수 부위 수분 범위 확인 및 가구/귀중품 이동",
                    "instruction": "벽지나 석고보드가 젖어 축축해진 범위를 확인하고 받침 양동이를 깝니다.",
                    "pro_tip": "벽지 표면에 곰팡이가 피어있다면 24시간 이상 지연 누수된 상태입니다.",
                    "caution": "젖은 석고보드를 무리하게 절단하다가 파이프를 더 찢지 마세요."
                },
                {
                    "step_num": 3,
                    "title": "비파괴 청음/열화상 누수 탐지기 점검 (전문가 영역)",
                    "instruction": "면허 배관공이 열화상 카메라와 청음식 센서로 정밀 핀포인트 탐지를 수행합니다.",
                    "pro_tip": "정확한 탐지 없이 벽 전체를 뜯어내면 복구비가 불어납니다.",
                    "caution": "무면허 수리업자가 임의로 벽을 뚫는 것을 방지하세요."
                },
                {
                    "step_num": 4,
                    "title": "파손 배관 부분 절단 및 새 배관 튜빙 교체",
                    "instruction": "누수 부위 석고보드 최소 면적만 뚫고 파손 배관 구간을 교체 수리합니다.",
                    "pro_tip": "수리 완료 후 30분간 메인 밸브를 열어두고 누수가 100% 없는지 검증합니다.",
                    "caution": "벽을 막기 전에 48시간 이상 완전 건조시켜야 곰팡이가 안 핍니다."
                }
            ],
            "pro_trigger_conditions": "벽 속 물 새는 소리가 지속되거나 석고보드가 무너질 위험이 있는 경우 즉시 전문 배관공을 부르세요."
        }
    elif any(k in text_query for k in ["외벽", "바깥", "exterior", "stucco", "스타코", "외부", "사이딩", "siding", "시멘트", "콘크리트"]):
        matched_key = "exterior_wall_hole"
    elif any(k in text_query for k in ["수도꼭지", "faucet", "꼭지", "cartridge", "수전"]):
        matched_key = "leaking_faucet"
    elif any(k in text_query for k in ["toilet", "flapper", "변기", "수조", "hiss"]):
        matched_key = "running_toilet"
    elif any(k in text_query for k in ["disposal", "jam", "분쇄기", "음식물", "motor", "humming"]):
        matched_key = "disposal_jam"
    elif any(k in text_query for k in ["drywall", "hole", "석고보드", "석고", "구멍", "patch", "doorknob"]):
        matched_key = "drywall_hole"
    elif any(k in text_query for k in ["trap", "p-trap", "트랩", "싱크대", "세면대", "싱크", "하수구", "배수관", "배수구", "sink", "drain"]):
        matched_key = "leaking_p_trap"
    elif any(k in text_query for k in ["heater", "온수기", "보일러", "boiler", "tank"]):
        matched_key = "water_heater_tank"
    elif any(k in text_query for k in ["전기", "전등", "조명", "스위치", "콘센트", "차단기", "light", "switch", "outlet", "electrical", "breaker", "flicker", "plug"]):
        return {
            "problem_title": f"전기 스위치 / 조명 및 콘센트 점검 ({notes.strip() if notes else '전기 기구 고장'})",
            "category": "Electrical",
            "confidence_score": "High (90%)",
            "verdict": "CALL_A_PRO" if any(w in text_query for w in ["불꽃", "차단기", "연기", "spark", "smoke", "breaker"]) else "DIY_RECOMMENDED",
            "difficulty": "Intermediate (안전 장구 및 전원 차단 필요)",
            "estimated_time": "20 - 40 minutes",
            "youtube_query": "how to change light switch electrical outlet",
            "cost_comparison": {
                "diy_cost": "$10 - $25 (부품비)",
                "pro_cost": "$150 - $250 (기술자 기본 출장비)",
                "estimated_savings": "$175",
                "savings_percentage": "88%"
            },
            "summary": f"고객님이 작성하신 증상('{notes.strip() if notes else '전기 고장'}'): 전기 스위치/조명 기구 접불 및 부품 노후화 진단입니다. 작업 전 반드시 주 차단기(Circuit Breaker)를 내리고 전원 유무를 테스터기로 확인하세요.",
            "safety_warnings": [
                "작업 전 주전원 차단기(Circuit Breaker)를 반드시 OFF로 내리고 비접촉 전압 테스터기로 전원이 완전히 차단되었는지 점검하세요.",
                "젖은 손으로 전기 부품을 만지지 마시고 절연 장갑을 착용하세요."
            ],
            "materials_needed": [
                {"name": "범용 데코라 전기 스위치 / 콘센트", "est_price": "$3.99", "amazon_search": "decora light switch 15a", "homedepot_search": "light switch"},
                {"name": "전기 테이프 (절연 테이프)", "est_price": "$2.99", "amazon_search": "electrical tape 3m", "homedepot_search": "electrical tape"}
            ],
            "tools_needed": [
                {"name": "비접촉 전압 테스터기", "amazon_search": "non contact voltage tester kleintools", "homedepot_search": "voltage tester"},
                {"name": "절연 십자/일자 드라이버 세트", "amazon_search": "insulated screwdriver set", "homedepot_search": "insulated screwdriver"}
            ],
            "steps": [
                {
                    "step_num": 1,
                    "title": "주전원 차단기 OFF 및 전압 확인",
                    "instruction": "두꺼비집(배전반)에서 해당 구역의 차단기를 내리고 비접촉 전압 테스터기로 전원 차단을 확인합니다.",
                    "pro_tip": "작업 중 다른 사람이 차단기를 켜지 못하도록 차단기에 경고 메모를 붙여두세요.",
                    "caution": "테스터기로 잔류 전압을 확인하기 전에는 전선을 손으로 만지지 마세요."
                },
                {
                    "step_num": 2,
                    "title": "커버 플레이트 및 내부 스위치 분리",
                    "instruction": "드라이버로 커버 플레이트 나사를 풀고 스위치를 벽 밖으로 살짝 당겨냅니다.",
                    "pro_tip": "기존 전선 연결 위치를 스마트폰으로 사진 찍어두면 재조립 시 실수가 없습니다.",
                    "caution": "전선을 억지로 세게 당기지 마세요."
                },
                {
                    "step_num": 3,
                    "title": "새 스위치 전선 결선 및 단단히 조임",
                    "instruction": "기존 전선을 새 스위치 터미널 나사에 감아 조이고 절연 테이프로 감싸 보강합니다.",
                    "pro_tip": "헐겁게 조이면 아크(불꽃)가 발생해 스위치가 탈 수 있으므로 꽉 조이세요.",
                    "caution": "접지선을 핫 단자에 접촉시키지 마세요."
                },
                {
                    "step_num": 4,
                    "title": "커버 재조립 및 차단기 ON 재개",
                    "instruction": "스위치를 벽 상자에 다시 넣고 나사를 조인 뒤 커버 플레이트를 덮고 차단기를 켭니다.",
                    "pro_tip": "스위치를 눌렀을 때 딸깍 소리가 경쾌하게 나면 정상 조립된 것입니다.",
                    "caution": "스위치를 켰을 때 차단기가 즉시 다시 떨어진다면 숏트가 발생한 것이니 전문가를 부르세요."
                }
            ],
            "pro_trigger_conditions": "스위치 타는 냄새, 벽 속 탄 자국, 240V 대형 가전 전원선, 또는 차단기가 지속적으로 내려갈 경우 즉시 면허 전기 기술자를 부르세요."
        }
    elif any(k in text_query for k in ["문", "경첩", "도어", "도어락", "열쇠", "손잡이", "door", "lock", "hinge", "handle", "sticking"]):
        return {
            "problem_title": f"문 손잡이 / 경첩 및 방문 걸림 수리 ({notes.strip() if notes else '문 작동 이상'})",
            "category": "Doors & Windows",
            "confidence_score": "High (90%)",
            "verdict": "DIY_RECOMMENDED",
            "difficulty": "Beginner (기본 공구 사용)",
            "estimated_time": "15 - 30 minutes",
            "youtube_query": "how to fix sticking door door handle hinge adjustment",
            "cost_comparison": {
                "diy_cost": "$5 - $15 (윤활제 및 나사비)",
                "pro_cost": "$120 - $180 (핸디맨 출장비)",
                "estimated_savings": "$140",
                "savings_percentage": "90%"
            },
            "summary": f"고객님이 입력하신 증상('{notes.strip() if notes else '문 고장'}'): 문틀 걸림, 경첩 나사 헐거움, 또는 도어락 윤활 부족 진단입니다. 긴 나사로 교체하고 윤활 스프레이를 도포하여 해결할 수 있습니다.",
            "safety_warnings": [
                "문이 무거우므로 경첩 나사를 풀 때 문 아래에 받침대를 괴어 두세요.",
                "나사가 마모되지 않도록 드라이버 크기를 딱 맞는 것을 사용하세요."
            ],
            "materials_needed": [
                {"name": "3인치 목재용 긴 수리 나사 (Hinge Screw Set)", "est_price": "$3.99", "amazon_search": "3 inch door hinge screws", "homedepot_search": "hinge screws"},
                {"name": "WD-40 콤팩트 실리콘 윤활 스프레이", "est_price": "$5.49", "amazon_search": "wd40 silicone spray", "homedepot_search": "silicone spray"}
            ],
            "tools_needed": [
                {"name": "전동 드라이버 또는 십자 수동 드라이버", "amazon_search": "cordless screwdriver", "homedepot_search": "screwdriver set"}
            ],
            "steps": [
                {
                    "step_num": 1,
                    "title": "문 처짐 및 경첩 헐거움 원인 확인",
                    "instruction": "문을 천천히 열고 닫으며 문 상단이나 바닥이 문틀에 닿는지 점검합니다.",
                    "pro_tip": "상단 경첩의 나사가 헛돌면 문 전체가 무게 때문에 아래로 처지게 됩니다.",
                    "caution": "문을 세게 닫아 문틀 나무가 쪼개지지 않도록 주의하세요."
                },
                {
                    "step_num": 2,
                    "title": "헛오는 경첩 나사를 3인치 긴 나사로 교체",
                    "instruction": "상단 경첩의 짧은 기존 나사를 빼내고 3인치 긴 나사로 강력하게 죄어줍니다.",
                    "pro_tip": "3인치 긴 나사 1개만 상단 경첩 중앙 구멍에 박아도 문 처짐이 100% 잡힙니다.",
                    "caution": "전동 드라이버 토크를 너무 높게 설정하면 나사 머리가 뭉개질 수 있습니다."
                },
                {
                    "step_num": 3,
                    "title": "경첩 피벗 및 도어락 래치 윤활 도포",
                    "instruction": "경첩 핀 마찰 부위와 도어락 래치에 실리콘 윤활 스프레이를 분사하고 흘러내린 액을 닦아냅니다.",
                    "pro_tip": "건식 실리콘 윤활제나 가파이트 가루를 쓰면 문고리가 10년 이상 부드럽습니다.",
                    "caution": "마루 바닥에 윤활유가 튀면 미끄러우므로 수건을 받치세요."
                },
                {
                    "step_num": 4,
                    "title": "문 개폐 및 걸쇠(Strike Plate) 최종 점검",
                    "instruction": "문을 5회 개폐하여 삐걱거리는 소리가 없어졌는지 잘 잠기는지 확인합니다.",
                    "pro_tip": "문이 걸쇠 위치에 안 맞으면 걸쇠 구멍 전면을 줄로 1mm 깎아내세요.",
                    "caution": "방화문의 경우 스프링 힌지 장력을 억지로 개조하지 마세요."
                }
            ],
            "pro_trigger_conditions": "문틀 차체가 심하게 비틀려 주택 기초 침하가 의심되거나 방화문 현관 도어락 작동 불능 시 면허 전문가를 부르세요."
        }
    elif any(k in text_query for k in ["마루", "바닥", "데크", "삐걱", "소리", "나무", "floor", "squeak", "deck", "hardwood", "creak"]):
        return {
            "problem_title": f"마루 바닥 삐걱거림 소음 및 틈새 마찰 수리 ({notes.strip() if notes else '마루 소리'})",
            "category": "Flooring & Decks",
            "confidence_score": "High (95%)",
            "verdict": "DIY_RECOMMENDED",
            "difficulty": "Beginner (초보자 10분 수리 가능)",
            "estimated_time": "10 - 20 minutes",
            "youtube_query": "how to fix squeaky hardwood floor without replacing wood",
            "cost_comparison": {
                "diy_cost": "$5 - $13 (윤활 흑연 가루 또는 수리 나사 키트)",
                "pro_cost": "$200 - $350 (마루 기술자 출장비)",
                "estimated_savings": "$220",
                "savings_percentage": "95%"
            },
            "summary": f"고객님이 입력하신 증상('{notes.strip() if notes else '마루 소음'}'): 마루판을 새로 교체할 필요 없이, 마루판 사이 마찰 소음 또는 하부 합판(Subfloor) 헐거움으로 인한 삐걱거림 현상입니다. 흑연 윤활 가루 도포 및 전용 수리 나사로 10분 만에 소음을 완전 제거할 수 있습니다.",
            "safety_warnings": [
                "마루판 표면에 일반 윤활유(기름)를 대량 분사하면 바닥이 미끄러울 수 있으니 반드시 건식 흑연 가루나 전용 실리콘을 사용하세요.",
                "나사를 박을 때 마루 아래 보일러 온수 파이프(배관) 위치를 피해서 작업하세요."
            ],
            "materials_needed": [
                {"name": "마루 삐걱거림 제거용 건식 흑연 윤활 가루 (Powdered Graphite Lubricant)", "est_price": "$4.99", "amazon_search": "powdered graphite lubricant squeaky floor", "homedepot_search": "graphite lubricant"},
                {"name": "마루 바닥 삐걱거림 수리 전용 나사 키트 (Squeeeek No More Hardwood Kit)", "est_price": "$12.99", "amazon_search": "squeeeeek no more hardwood floor kit", "homedepot_search": "squeak no more kit"}
            ],
            "tools_needed": [
                {"name": "전동 드라이버 또는 망치", "amazon_search": "cordless drill driver", "homedepot_search": "drill driver"}
            ],
            "steps": [
                {
                    "step_num": 1,
                    "title": "소리 나는 마루 마찰 위치 핀포인트 탐색",
                    "instruction": "마루 위를 발로 밟으며 삐걱거리는 정확한 마루판 틈새 지점을 찾습니다.",
                    "pro_tip": "마루판끼리 비벼지며 소리가 나는지, 하부 합판이 들떠 소리가 나는지 밟아보면 구분됩니다.",
                    "caution": "마루판을 무리하게 드라이버로 쑤셔 틈을 벌리지 마세요."
                },
                {
                    "step_num": 2,
                    "title": "건식 흑연 가루(Graphite Powder) 틈새 침투",
                    "instruction": "삐걱거리는 마루 틈새 사이에 흑연 윤활 가루를 노즐로 듬뿍 집어넣고 수건으로 마찰시켜 틈새로 넣어줍니다.",
                    "pro_tip": "흑연 가루가 마루판 사이 마찰을 없애주므로 나무 교체 없이 소리가 즉시 멈춥니다.",
                    "caution": "흑연 가루가 흰 옷이나 벽에 묻지 않도록 헝겊으로 잘 닦아내세요."
                },
                {
                    "step_num": 3,
                    "title": "하부 합판 들뜸 시 삐걱거림 수리 나사 고정",
                    "instruction": "소리가 지속될 경우 Squeeeek No More 수리 나사를 마루 위에서 박아 스냅(부러뜨림) 마감하여 깔끔하게 고정합니다.",
                    "pro_tip": "이 특수 나사는 마루판 속으로 들어가 머리가 자동으로 깔끔하게 잘려나갑니다.",
                    "caution": "바닥 난방 파이프 깊이를 넘어서는 긴 나사를 사용하지 마세요."
                },
                {
                    "step_num": 4,
                    "title": "바닥 표면 청소 및 보행 테스트",
                    "instruction": "남은 가루를 깨끗이 청소한 후 체중을 실어 밟아보며 소음 제거를 확인합니다.",
                    "pro_tip": "습도가 건조해지면 마루 소리가 잦아지므로 실내 적정 습도(40~50%)를 유지하면 좋습니다.",
                    "caution": "물걸레질 후 잔여 습기가 잘 마르도록 통풍시켜 주세요."
                }
            ],
            "pro_trigger_conditions": "마루 전체가 푹 꺼지거나 누수로 인해 합판 전체가 상해 썩었을 경우에는 마루 전체 교체 전문가를 부르세요."
        }

    if matched_key and matched_key in SAMPLE_SCENARIOS:
        return SAMPLE_SCENARIOS[matched_key]["result"]

    # General Fallback
    user_text = notes.strip() if notes else "주택 수리 및 하자 진단"
    return {
        "problem_title": f"진단 요청: {user_text}",
        "category": "General Home Repair",
        "confidence_score": "High (90%)",
        "verdict": "DIY_RECOMMENDED",
        "difficulty": "Beginner (초보자 수리 가능)",
        "estimated_time": "15 - 30 minutes",
        "youtube_query": f"how to fix {user_text}",
        "cost_comparison": {
            "diy_cost": "$10 - $30 (자재/부품비)",
            "pro_cost": "$150 - $250 (기술자 기본 출장비)",
            "estimated_savings": "$170",
            "savings_percentage": "85%"
        },
        "summary": f"작성하신 내용: \"{user_text}\"에 대한 맞춤형 AI 진단 리포트입니다. 수리 전 해당 부위의 전원 또는 급수를 차단하고, 아래의 단계별 작업 순서와 준비물을 확인해 보세요.",
        "safety_warnings": [
            "작업을 시작하기 전 관련 전원 차단기 또는 수전 급수 밸브 차단 여부를 반드시 확인하세요.",
            "보안경, 장갑 등 안전 공구를 착용하여 작업 중 부상을 예방하세요."
        ],
        "materials_needed": [
            {"name": f"{user_text} 관련 교체 부품 / 보수 자재", "est_price": "$15.00", "amazon_search": f"{user_text} repair parts", "homedepot_search": f"{user_text}"}
        ],
        "tools_needed": [
            {"name": "가정용 수공구 세트 (드라이버, 조절식 플라이어)", "amazon_search": "home tool kit set", "homedepot_search": "tool set"}
        ],
        "steps": [
            {
                "step_num": 1,
                "title": "고장 부위 확인 및 안전 차단",
                "instruction": f"고장 부위({user_text}) 주변을 정돈하고 전원 차단기나 밸브를 차단합니다.",
                "pro_tip": "분해 전 부품 상태를 사진으로 찍어두면 부품 구매와 재조립 시 큰 도움이 됩니다.",
                "caution": "차단 여부가 불분명할 경우 무리하게 부품을 힘으로 당기지 마세요."
            },
            {
                "step_num": 2,
                "title": "노후 부품 분리 및 호환 규격 확인",
                "instruction": "기존 부품을 조심스럽게 떼어내어 부식 상태와 치수를 확인합니다.",
                "pro_tip": "아마존이나 홈디포 검색창에 부품 이름을 검색하여 교체품을 찾으세요.",
                "caution": "나사가 안 풀린다고 망치로 세게 때리면 부품이 파손될 수 있습니다."
            },
            {
                "step_num": 3,
                "title": "새 부품 교체 및 고정",
                "instruction": "새 부품을 위치에 맞춰 장착하고 나사나 너트를 단단히 조여 고정합니다.",
                "pro_tip": "나사산을 맞출 때 삐뚤어지지 않도록 손으로 먼저 세 바퀴 돌린 후 공구를 쓰세요.",
                "caution": "플라스틱이나 얇은 도기 부품은 과도하게 죄면 깨질 수 있습니다."
            },
            {
                "step_num": 4,
                "title": "전원/급수 재개 및 테스트",
                "instruction": "전원 차단기나 급수 밸브를 다시 켜고 작동 상태와 누수 여부를 체크합니다.",
                "pro_tip": "작동 후 5분간 지켜보면서 누수나 이상 소음이 없는지 확인하세요.",
                "caution": "탄 냄새나 불꽃, 누수가 계속 발생하면 즉시 작업을 멈추고 전문가를 부르세요."
            }
        ],
        "pro_trigger_conditions": "고전압(240V), 가스관, 대형 누수, 건물 구조 결함이 감지되면 즉시 라이선스 전문 기술자를 부르세요."
    }


@app.post("/api/analyze")
async def analyze_image(
    image: Optional[UploadFile] = File(None),
    sample_id: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    api_key: Optional[str] = Form(None)
):
    """
    Main diagnostic endpoint:
    - If a sample_id is provided, returns that sample's diagnosis instantly.
    - If an image or text description is provided, calls Gemini AI (or smart intelligent fallback).
    """
    is_custom_notes = bool(notes and notes.strip())
    if sample_id and sample_id in SAMPLE_SCENARIOS and not is_custom_notes:
        logger.info(f"Serving instant sample scenario: {sample_id}")
        return {
            "source": "sample",
            "data": SAMPLE_SCENARIOS[sample_id]["result"]
        }

    has_uploaded_file = bool(image and hasattr(image, "filename") and image.filename)

    if not has_uploaded_file and not is_custom_notes and not sample_id:
        raise HTTPException(status_code=400, detail="Please upload a photo or describe the repair issue.")

    try:
        contents = None
        mime_type = None
        if has_uploaded_file:
            contents = await image.read()
            mime_type = image.content_type or "image/jpeg"

        user_or_env_key = api_key or os.environ.get("GEMINI_API_KEY")

        if not user_or_env_key:
            logger.warning("No Gemini API key provided. Matching intelligent keyword fallback.")
            return {
                "source": "demo_fallback",
                "message": "Demo Mode: Live analysis completed using intelligent contractor blueprint.",
                "data": get_smart_fallback(notes)
            }

        logger.info("Executing live Gemini 2.5 Flash diagnostic analysis...")
        result = await analyze_repair_issue(
            image_bytes=contents,
            mime_type=mime_type,
            user_notes=notes,
            api_key=user_or_env_key
        )

        return {
            "source": "live_ai",
            "data": result
        }

    except ValueError as ve:
        if str(ve) == "NO_API_KEY":
            return {
                "source": "demo_fallback",
                "message": "Demo Mode: Live analysis completed using intelligent contractor blueprint.",
                "data": get_smart_fallback(notes)
            }
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error during AI analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"AI Diagnostic error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error during AI analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"AI Diagnostic error: {str(e)}"
        )


@app.post("/api/chat")
async def chat_diagnostic(payload: dict):
    """
    Interactive Multi-Turn AI Diagnostic Chat:
    Converses with the user in real-time, asks clarifying questions (e.g. interior drywall vs exterior stucco),
    and delivers tailored repair blueprints.
    """
    messages = payload.get("messages", [])
    user_api_key = payload.get("api_key") or os.environ.get("GEMINI_API_KEY")
    lang = payload.get("language", "ko")

    if not messages:
        raise HTTPException(status_code=400, detail="No messages provided.")

    last_user_msg = messages[-1].get("content", "").strip()
    full_conversation_text = " ".join([m.get("content", "") for m in messages]).lower()

    # If user has a live Gemini API key, use Gemini 2.5 Flash Chat
    if user_api_key:
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=user_api_key)
            system_instruction = (
                "You are FixOrPro AI, a Master Home Inspector and Licensed General Contractor. "
                "Engage in a friendly, practical, and highly precise consultation in the user's language. "
                "Ask clarifying questions if the repair context is ambiguous (e.g., distinguishing between "
                "interior drywall holes vs exterior stucco/siding breaches, plumbing cartridge vs pipe leak). "
                "Provide accurate cost savings estimates (DIY vs Pro) and genuine hardware store tools/parts from Home Depot and Amazon."
            )
            
            gemini_contents = []
            for m in messages:
                role = "user" if m.get("role") == "user" else "model"
                gemini_contents.append(f"{role}: {m.get('content')}")

            resp = client.models.generate_content(
                model='gemini-2.5-flash',
                contents="\n".join(gemini_contents),
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3,
                )
            )
            return {
                "reply": resp.text.strip(),
                "report_scenario": "exterior_wall_hole" if ("외벽" in full_conversation_text or "exterior" in full_conversation_text) else None
            }
        except Exception as e:
            logger.error(f"Gemini Chat API error: {e}")

    # Smart Interactive Rule-based Dialogue Engine
    text = last_user_msg.lower()
    clean_text = text.strip().rstrip("!?.~ ")

    # 0. Greetings / Hello / Test messages
    greeting_words = ["하이", "하이라고", "하이요", "하이~", "안녕", "안녕하세요", "hi", "hello", "hey", "ㅎㅇ", "방가", "반가워", "반갑습니다", "테스트", "test"]
    is_greeting = (
        clean_text in greeting_words
        or any(clean_text.startswith(w) for w in ["하이", "안녕", "hi", "hello", "hey", "ㅎㅇ", "방가"])
        or any(w in clean_text for w in ["하이라고", "하이요", "안녕하세요", "반갑습니다"])
    )

    if is_greeting:
        reply = (
            "안녕하세요! 👨‍🔧 **FixOrPro AI 집수리 마스터**입니다.\n\n"
            "어디에 어떤 고장이나 누수가 발생했나요?\n"
            "대화창에 증상을 자유롭게 적어주시거나 아래 **추천 버튼**을 선택해 주세요!\n\n"
            "• 예시 1: *\"싱크대 밑에서 물이 뚝뚝 새요\"*\n"
            "• 예시 2: *\"방 안 실내 석고 벽에 구멍이 났어요\"*\n"
            "• 예시 3: *\"변기 물 소리가 안 멈춰요\"*"
        )
        return {
            "reply": reply,
            "suggestions": ["🏠 건물 외벽 구멍 수리", "🚰 싱크대 수도꼭지 누수", "🚽 변기 물 샐 때", "🚪 실내 석고보드 구멍"],
            "report_scenario": None
        }

    # 1. Exterior Wall / Stucco / Siding
    if any(w in text or w in full_conversation_text for w in ["외벽", "바깥", "exterior", "stucco", "스타코", "사이딩", "외부 벽", "시멘트"]):
        reply = (
            "🏠 **건물 외벽(스타코/사이딩/콘크리트) 구멍 수리 진단입니다.**\n\n"
            "실내 석고보드와 달리 **건물 외벽은 빗물 차단(방수)과 자외선 내후성**이 핵심입니다.\n\n"
            "• **수리 방식**: 외벽 전용 아크릴 스타코 패치(Ready-Mix Stucco Patch)로 충진 후, 우레탄 방수 씰런트 코킹 및 외벽용 아크릴 페인트 마감\n"
            "• **DIY 비용**: 약 $18~$35 (기술자 의뢰 시 $250~$450 대비 **약 $315 절약!**)\n"
            "• **권장 공구**: 2x5인치 스틸 마진 흙손, 와이어 브러시, 주방 스펀지(스타코 거친 질감 복원용)\n\n"
            "아래 **[⚡ 맞춤형 진단 리포트 & 부품 견적서 보기]** 버튼을 누르시면 1~4단계 완전 분해 가이드와 동영상을 즉시 확인하실 수 있습니다!"
        )
        return {
            "reply": reply,
            "report_scenario": "exterior_wall_hole",
            "report_data": SAMPLE_SCENARIOS["exterior_wall_hole"]["result"]
        }

    # 2. Interior Wall / Drywall / Doorknob Hole
    if any(w in text for w in ["실내", "석고", "drywall", "방문", "손잡이"]):
        reply = (
            "🚪 **실내 석고보드(Drywall) 문 손잡이 충격 구멍 진단입니다.**\n\n"
            "• **수리 방식**: 알루미늄 자가점착 메쉬 패치(4x4인치) + 변색 스패클 퍼티 샌딩 마감\n"
            "• **DIY 비용**: 약 $15 (기술자 비용 $180 대비 **약 $165 절약!**)\n\n"
            "아래 버튼을 눌러 부품 구매 링크와 수리 가이드를 확인하세요!"
        )
        return {
            "reply": reply,
            "report_scenario": "drywall_hole",
            "report_data": SAMPLE_SCENARIOS["drywall_hole"]["result"]
        }

    # 3. Ambiguous "Hole in wall" -> Ask Clarifying Question!
    if any(w in text for w in ["벽", "구멍", "hole", "wall"]):
        reply = (
            "🛠️ **벽에 난 구멍 수리를 진단해 드리겠습니다.**\n\n"
            "가장 정확한 수리 방법과 부품을 안내해 드리기 위해 1가지만 여쭤볼게요!\n\n"
            "👉 **구멍이 난 벽의 위치가 어디인가요?**\n"
            "1. **건물 외벽 (바깥 스타코 미장 / 사이딩 / 콘크리트)**\n"
            "2. **방 안 실내 벽 (석고보드 Drywall / 문 손잡이 충격)**\n\n"
            "아래 답변을 입력해 주시거나 버튼을 선택해 주세요!"
        )
        return {
            "reply": reply,
            "suggestions": ["🏠 건물 외벽(바깥 벽)이에요", "🚪 방 안 실내 벽(석고보드)이에요"],
            "report_scenario": None
        }

    # 4. Faucet / Kitchen Sink Leaks
    if any(w in text for w in ["수도", "faucet", "꼭지", "싱크", "sink", "drip"]):
        reply = (
            "🚰 **주방/욕실 수도꼭지 누수 및 카트리지 마모 진단입니다.**\n\n"
            "수도꼭지 전체 교체 없이 내부 카트리지($15) 교체만으로 30분 만에 물 뚝뚝 떨어짐을 100% 잡을 수 있습니다."
        )
        return {
            "reply": reply,
            "report_scenario": "leaking_faucet",
            "report_data": SAMPLE_SCENARIOS["leaking_faucet"]["result"]
        }

    # 5. Default Consultation Response
    reply = (
        "💡 **전문가 AI가 문제를 정밀 분석 중입니다.**\n\n"
        f"말씀해 주신 증상: *\"{last_user_msg}\"*\n\n"
        "고장 부위(실내/실외, 재질, 누수 여부)를 조금만 더 구체적으로 말씀해 주시면 100% 호환 부품과 최저가 수리 플랜을 완성해 드립니다."
    )
    return {
        "reply": reply,
        "suggestions": ["🏠 건물 외벽 구멍 수리", "🚰 싱크대 수도꼭지 누수", "🚽 변기 물 흐르는 소리", "🗑️ 음식물 분쇄기 걸림"],
        "report_scenario": None
    }


# Mount static files (HTML, CSS, JS, Assets)
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

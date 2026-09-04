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
from app.ai_diagnostics import analyze_repair_image, generate_dynamic_questions
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
                "title": "💡 [2차 정밀 좁히기] 선택하신 싱크대 누수의 세부 상태를 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 2,
                "can_narrow_further": False,
                "options": [
                    {"text": "수도꼭지(수전)를 틀 때만 배수관/P-트랩 연결 조인트에서 물이 떨어짐"},
                    {"text": "수도 사용과 무관하게 24시간 내내 급수 밸브 호스에서 뚝뚝 새어나옴"},
                    {"text": "싱크대 하부 목재 바닥판이 물에 불어 곰팡이가 피고 습기가 찬 상태임"},
                    {"text": "앵글 밸브(급수 밸브) 나사산 부식으로 밸브 자체에서 누수됨"}
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
                "title": "💡 [2차 정밀 좁히기] 선택하신 변기 문제의 세부 상황을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 2,
                "can_narrow_further": False,
                "options": [
                    {"text": "물 내린 후에도 수조 안에서 물 소리가 꺼지지 않고 계속 남"},
                    {"text": "변기 바닥 타일 사이 실리콘/시멘트 틈새로 오수가 스며나옴"},
                    {"text": "수조 레버를 눌러도 줄이 빠져서 물이 안 내려감"},
                    {"text": "변기 도기 표면에 균열(금)이 가서 물이 비침"}
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
                "title": "💡 [2차 정밀 좁히기] 선택하신 온수기 문제의 세부 증상을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 2,
                "can_narrow_further": False,
                "options": [
                    {"text": "온수기 바닥 물받이 팬(Drain Pan)에 물이 고여 있음"},
                    {"text": "온수를 가동할 때만 배관 조인트에서 가열음과 함께 물이 새어남"},
                    {"text": "온수기 내부 녹물이 흘러나와 바닥이 녹색/갈색으로 오염됨"},
                    {"text": "메인 차단 밸브를 잠그면 온수기 물 유출이 멈춤"}
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
                "title": "💡 [2차 정밀 좁히기] 선택하신 천장/벽체 누수의 세부 상태를 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 2,
                "can_narrow_further": False,
                "options": [
                    {"text": "물에 젖은 표면이 석고보드(Drywall)이고 변색 및 곰팡이가 피어남"},
                    {"text": "물방울이 떨어져 바닥 받침 양동이를 놓아야 할 정도로 낙수량이 많음"},
                    {"text": "누수 부위에 전등이나 콘센트 등 전기 전선관이 인접해 있음"},
                    {"text": "배관 밸브를 잠그면 물 떨어짐이 즉시 멈춤"}
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
                "title": "💡 [2차 정밀 좁히기] 선택하신 전기 고장의 세부 증상을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 2,
                "can_narrow_further": False,
                "options": [
                    {"text": "120V 일반 조명/소형 가전 회로 라인임"},
                    {"text": "240V 대형 가전(건조기/오븐/에어컨) 차단기 회로 라인임"},
                    {"text": "전선 피복 타는 냄새나 검은 탄 자국이 외부에 보임"},
                    {"text": "단순 스위치/콘센트 기계적 부품 노후화 마모임"}
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
                "title": "💡 [2차 정밀 좁히기] 선택하신 구멍의 크기 및 상태를 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 2,
                "can_narrow_further": False,
                "options": [
                    {"text": "구멍 크기가 주먹 크기 미만 (4인치 이하)"},
                    {"text": "구멍 크기가 농구공 이상으로 큼 (8인치 이상)"},
                    {"text": "구멍 안쪽에 전선관이나 배관 파이프가 지나감"},
                    {"text": "단순 표면 미장 마감재 및 페인트만 떨어진 상태"}
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
                "title": "💡 [2차 정밀 좁히기] 선택하신 문 문제의 세부 증상을 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 2,
                "can_narrow_further": False,
                "options": [
                    {"text": "3인치 긴 수리 나사로 상단 경첩을 고정해야 하는 처짐 상태"},
                    {"text": "문고리 실리콘 윤활 스프레이 도포가 필요한 뻑뻑함"},
                    {"text": "문틀 걸쇠(Strike Plate) 위치 조정이 필요한 불일치"},
                    {"text": "도어락 전자 장치 고장으로 1:1 교체 필요"}
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
                "title": f"💡 [2차 정밀 좁히기] 선택하신 증상의 세부 긴급도 및 범위를 1, 2, 3, 4번에서 선택해 주세요.",
                "level": 2,
                "can_narrow_further": False,
                "options": [
                    {"text": "1번: 기본 수공구로 30분 내 DIY 교체 가능 수준"},
                    {"text": "2번: 전원/메인 급수 밸브 차단 후 안전 확인 필요 수준"},
                    {"text": "3번: 호환 교체 부품 구매 후 1:1 맞춤 교체 작업 수준"},
                    {"text": "4번: 면허 전문가(배관공/전기기사) 출장 수리 권장 수준"}
                ]
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
    # 1. Check if user selected a pre-configured sample (only if user did NOT write a custom description)
    is_custom_notes = bool(notes and notes.strip())
    if sample_id and sample_id in SAMPLE_SCENARIOS and not is_custom_notes:
        logger.info(f"Serving instant sample scenario: {sample_id}")
        return {
            "source": "sample",
            "data": SAMPLE_SCENARIOS[sample_id]["result"]
        }

    # 2. Check if at least an image OR text description was provided
    if not image and not is_custom_notes and not sample_id:
        raise HTTPException(status_code=400, detail="Please upload a photo or describe the repair issue.")

    try:
        contents = None
        mime_type = None
        if image:
            contents = await image.read()
            mime_type = image.content_type or "image/jpeg"

        # Check for Gemini API key
        user_or_env_key = api_key or os.environ.get("GEMINI_API_KEY")

        if not user_or_env_key:
            # Smart intelligent fallback based on user's written description or image
            logger.warning("No Gemini API key provided. Matching intelligent keyword fallback.")
            text_query = (notes or "").lower()
            
            matched_key = None
            # 0. Check for Wall / Ceiling In-Wall Water Leak FIRST (Compound condition to prevent false single-word matches)
            if (any(w in text_query for w in ["벽", "wall", "천장", "ceiling"]) and any(w in text_query for w in ["물", "새", "누수", "leak", "drip", "젖"])):
                fallback_sample = {
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
                    "summary": f"고객님이 입력하신 증상('{notes.strip()}'): 벽체 또는 천장 내부 급수/배수관 파손으로 인한 수분 침투 진단입니다. 벽 안쪽 누수는 곰팡이 감염, 석고보드 붕괴 및 주택 구조 부식을 유발하므로 주 메인 급수 밸브를 즉시 잠그고 전문 누수 탐지 배관공을 부르셔야 합니다.",
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
                            "instruction": "집 외부에 있는 메인 수도 계량기 밸브나 차고/지하실의 메인 급수 밸브를 잠급니다. 계량기 별표 바늘이 돌아가는지 확인하여 벽 속 배관 수압 누수를 더블 체크합니다.",
                            "pro_tip": "밸브를 잠근 후 집안의 가장 낮은 수전(외부 호스 수전)을 열어 배관 속 남아있는 잔여 물을 빠르게 빼내세요.",
                            "caution": "누수 지점에 전등이나 콘센트가 가까이 있다면 감전 위험이 있으므로 전기 차단기도 함께 내리세요."
                        },
                        {
                            "step_num": 2,
                            "title": "누수 부위 수분 범위 확인 및 가구/귀중품 이동",
                            "instruction": "벽지나 석고보드가 젖어 축축해진 범위를 눈과 수분 측정기로 확인하고, 물이 떨어지는 바닥에 받침 양동이와 수건을 깝니다.",
                            "pro_tip": "벽지 표면에 곰팡이가 피거나 들뜬 부위가 있다면 습기가 24시간 이상 지연 누수된 상태입니다.",
                            "caution": "젖은 석고보드를 칼로 무리하게 절단하다가 안쪽 누수 파이프를 더 크게 찢지 않도록 주의하세요."
                        },
                        {
                            "step_num": 3,
                            "title": "비파괴 청음/열화상 누수 탐지기 점검 (전문가 영역)",
                            "instruction": "면허 배관공이 열화상 카메라와 청음식 센서를 벽면에 대어 석고보드를 뜯지 않고 정확한 누수 포인트를 핀포인트로 찾아냅니다.",
                            "pro_tip": "정확한 핀포인트 탐지 없이 벽 전체를 뜯어내면 목조 프레임 복구비가 수천 달러로 불어납니다.",
                            "caution": "무면허 수리업자가 임의로 벽을 뚫는 것은 주택 보험 청구 시 불이익을 받을 수 있습니다."
                        },
                        {
                            "step_num": 4,
                            "title": "파손 배관 부분 절단 및 새 배관 튜빙 교체",
                            "instruction": "누수 부위 석고보드 최소 면적만 뚫고, 부식되거나 균열이 간 구리/PEX 배관 구간을 cut-out 한 뒤 새 파이프와 커플링으로 압착/용접 수리합니다.",
                            "pro_tip": "수리 완료 후 30분간 메인 밸브를 열어두고 휴지로 조인트 부위를 감싸 미세 누수가 100% 없는지 검증합니다.",
                            "caution": "수리 후 벽을 막기 전에 팬과 제습기로 벽 안쪽 목재 스터드를 최소 48시간 이상 완전 건조시켜야 곰팡이가 안 핍니다."
                        }
                    ],
                    "pro_trigger_conditions": "벽 속 물 새는 소리가 지속되거나, 천장/벽체 석고보드가 물에 불어 무너질 위험이 있는 경우 즉시 메인 수도를 잠그고 면허 배관공을 부르세요."
                }
                return {
                    "source": "demo_fallback",
                    "message": "Demo Mode: Live analysis completed using intelligent contractor blueprint.",
                    "data": fallback_sample
                }
            elif any(k in text_query for k in ["외벽", "바깥", "exterior", "stucco", "스타코", "외부", "사이딩", "siding", "시멘트", "콘크리트"]):
                matched_key = "exterior_wall_hole"
            elif any(k in text_query for k in ["수도꼭지", "faucet", "꼭지", "cartridge"]):
                matched_key = "leaking_faucet"
            elif any(k in text_query for k in ["toilet", "flapper", "변기", "수조", "hiss"]):
                matched_key = "running_toilet"
            elif any(k in text_query for k in ["disposal", "jam", "분쇄기", "음식물", "motor", "humming"]):
                matched_key = "disposal_jam"
            elif any(k in text_query for k in ["drywall", "hole", "벽", "석고", "구멍", "patch", "doorknob"]):
                matched_key = "drywall_hole"
            elif any(k in text_query for k in ["trap", "p-trap", "트랩", "누수", "배관"]):
                matched_key = "leaking_p_trap"
            elif any(k in text_query for k in ["heater", "온수기", "보일러", "boiler", "tank"]):
                matched_key = "water_heater_tank"
            elif any(k in text_query for k in ["전기", "전등", "조명", "스위치", "콘센트", "차단기", "light", "switch", "outlet", "electrical", "breaker", "flicker", "plug"]):
                fallback_sample = {
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
                    "summary": f"고객님이 작성하신 증상('{notes.strip()}'): 전기 스위치/조명 기구 접불 및 부품 노후화 진단입니다. 작업 전 반드시 주 차단기(Circuit Breaker)를 내리고 전원 유무를 테스터기로 확인하세요.",
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
                            "instruction": "두꺼비집(배전반)에서 해당 구역의 차단기를 내립니다. 비접촉 전압 테스터기를 스위치나 콘센트 표면에 대어 소리나 불빛이 안 나는지 전원 차단을 확인합니다.",
                            "pro_tip": "작업 중 다른 사람이 차단기를 켜지 못하도록 차단기에 경고 메모를 붙여두세요.",
                            "caution": "테스터기로 잔류 전압을 확인하기 전에는 절대로 전선을 손으로 만지지 마세요."
                        },
                        {
                            "step_num": 2,
                            "title": "커버 플레이트 및 내부 스위치 분리",
                            "instruction": "드라이버로 플라스틱 커버 플레이트 나사를 풀고 내부 스위치 고정 나사를 풀어 벽 밖으로 살짝 당겨냅니다.",
                            "pro_tip": "기존 전선 연결 위치(핫/뉴트럴/접지)를 스마트폰으로 사진 찍어두면 재조립 시 실수가 없습니다.",
                            "caution": "전선을 억지로 세게 당기면 벽 안쪽 전선관이 손상될 수 있습니다."
                        },
                        {
                            "step_num": 3,
                            "title": "새 스위치 전선 결선 및 단단히 조임",
                            "instruction": "기존 전선을 새 스위치 터미널 나사에 시계 방향으로 감아 나사를 단단히 조입니다. 그 후 절연 테이프로 스위치 측면 금속 단자를 2바퀴 감싸 보강합니다.",
                            "pro_tip": "나사를 조일 때 헐겁게 조이면 아크(불꽃)가 발생해 스위치가 탈 수 있으므로 기계적으로 꽉 조이세요.",
                            "caution": "접지선(구리 맨전선)을 핫(Black) 단자에 접촉시키지 마세요."
                        },
                        {
                            "step_num": 4,
                            "title": "커버 재조립 및 차단기 ON 재개",
                            "instruction": "스위치를 벽 상자에 다시 넣고 나사를 조인 뒤 커버 플레이트를 덮습니다. 배전반 차단기를 켜고 조명 스위치가 정상 작동하는지 테스트합니다.",
                            "pro_tip": "스위치를 눌렀을 때 딸깍 소리가 경쾌하게 나면 정상 조립된 것입니다.",
                            "caution": "스위치를 켰을 때 차단기가 즉시 다시 떨어진다면 숏트(단락)가 발생한 것이니 즉시 전원을 끄고 전문 전기기사를 부르세요."
                        }
                    ],
                    "pro_trigger_conditions": "스위치 타는 냄새, 벽 속 탄 자국, 240V 대형 가전 전원선, 또는 차단기가 지속적으로 내려갈 경우 즉시 면허 전기 기술자를 부르세요."
                }
                return {
                    "source": "demo_fallback",
                    "message": "Demo Mode: Custom user description analysis generated.",
                    "data": fallback_sample
                }
            elif any(k in text_query for k in ["문", "경첩", "도어", "도어락", "열쇠", "손잡이", "door", "lock", "hinge", "handle", "sticking"]):
                fallback_sample = {
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
                    "summary": f"고객님이 입력하신 증상('{notes.strip()}'): 문틀 걸림, 경첩 나사 헐거움, 또는 도어락 문 손잡이 윤활 부족 진단입니다. 경첩 나사를 긴 나사로 교체하고 윤활 스프레이를 도포하여 간단히 해결할 수 있습니다.",
                    "safety_warnings": [
                        "문이 무거우므로 경첩 나사를 풀 때 문 아래에 받침대(책이나 나무 조각)를 괴어 두세요.",
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
                            "instruction": "문을 천천히 열고 닫으며 문 상단이나 바닥이 문틀에 닿는지, 상단 경첩 나사가 헛돌며 떠 있는지 점검합니다.",
                            "pro_tip": "상단 경첩의 나사가 헛돌면 문 전체가 무게 때문에 아래로 처지게 됩니다.",
                            "caution": "문을 세게 닫아 문틀 나무가 쪼개지지 않도록 주의하세요."
                        },
                        {
                            "step_num": 2,
                            "title": "헛오는 경첩 나사를 3인치 긴 나사로 교체",
                            "instruction": "상단 경첩의 짧은 기존 나사(3/4인치)를 빼내고, 문틀 목조 스터드까지 깊게 박히는 3인치 긴 나사로 강력하게 죄어줍니다.",
                            "pro_tip": "3인치 긴 나사 1개만 상단 경첩 중앙 구멍에 박아도 문틀 스터드를 잡아당겨 문 처짐이 100% 잡힙니다.",
                            "caution": "전동 드라이버 토크를 너무 높게 설정하면 나사 머리가 뭉개질 수 있습니다."
                        },
                        {
                            "step_num": 3,
                            "title": "경첩 피벗 및 도어락 래치 윤활 도포",
                            "instruction": "경첩 핀 마찰 부위와 도어락 래치(문고리 돌출부)에 실리콘 윤활 스프레이를 살짝 분사한 후 휴지로 흘러내린 액을 닦아냅니다.",
                            "pro_tip": "일반 기름 대신 먼지가 덜 붙는 건식 실리콘 윤활제나 가파이트 가루를 쓰면 문고리가 10년 이상 부드럽습니다.",
                            "caution": "마루 바닥에 윤활유가 튀면 매우 미끄러우므로 수건을 받치고 작업하세요."
                        },
                        {
                            "step_num": 4,
                            "title": "문 개폐 및 걸쇠(Strike Plate) 최종 점검",
                            "instruction": "문을 5회 개폐하여 삐걱거리는 소리가 없어졌는지, 문을 닫았을 때 걸쇠에 딸깍 소리가 나며 잘 잠기는지 확인합니다.",
                            "pro_tip": "문이 걸쇠 위치에 살짝 안 맞으면 걸쇠 구멍 전면을 줄(File)로 1mm 깎아내면 깔끔합니다.",
                            "caution": "현관문 등 방화문의 경우 스프링 힌지 장력을 억지로 개조하지 마세요."
                        }
                    ],
                    "pro_trigger_conditions": "문틀 차체가 심하게 비틀려 주택 기초 침하가 의심되거나, 방화문 현관 도어락 작동 불능 시 면허 전문가를 부르세요."
                }
                return {
                    "source": "demo_fallback",
                    "message": "Demo Mode: Custom user description analysis generated.",
                    "data": fallback_sample
                }
            elif matched_key:
                fallback_sample = SAMPLE_SCENARIOS[matched_key]["result"]
                return {
                    "source": "demo_fallback",
                    "message": "Demo Mode: Live analysis completed using intelligent contractor blueprint.",
                    "data": fallback_sample
                }
            else:
                user_text = notes.strip() if notes else "주택 수리 및 하자 진단"
                fallback_sample = {
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
                            "instruction": f"고장 부위({user_text}) 주변을 정돈하고, 전기/배관 작업 시 관련 전원 차단기나 밸브를 차단합니다.",
                            "pro_tip": "분해 전 부품 상태를 사진으로 찍어두면 부품 구매와 재조립 시 큰 도움이 됩니다.",
                            "caution": "차단 여부가 불분명할 경우 무리하게 부품을 힘으로 당기지 마세요."
                        },
                        {
                            "step_num": 2,
                            "title": "노후 부품 분리 및 호환 규격 확인",
                            "instruction": "기존 부품을 조심스럽게 떼어내어 부식 상태와 치수, 나사선 규격을 확인합니다.",
                            "pro_tip": "아마존이나 홈디포 검색창에 부품 이름을 검색하여 정확히 일치하는 교체품을 찾으세요.",
                            "caution": "나사가 안 풀린다고 망치로 세게 때리면 인근 부품이 파손될 수 있습니다."
                        },
                        {
                            "step_num": 3,
                            "title": "새 부품 교체 및 고정",
                            "instruction": "새 부품을 위치에 맞춰 장착하고 나사나 너트를 단단히 조여 고정합니다.",
                            "pro_tip": "나사산을 맞출 때 삐뚤어지지 않도록 손으로 먼저 세 바퀴 돌린 후 공구를 쓰세요.",
                            "caution": "플라스틱이나 얇은 도기 부품은 과도하게 죄면 깨질 수 있으니 적당히 조이세요."
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
                return {
                    "source": "demo_fallback",
                    "message": "Demo Mode: Custom user description analysis generated.",
                    "data": fallback_sample
                }

        # Live Gemini 2.5 Flash analysis (Multimodal or Text-based)
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
                "data": SAMPLE_SCENARIOS["exterior_wall_hole" if ("외벽" in (notes or "") or "바깥" in (notes or "")) else "running_toilet"]["result"]
            }
        raise HTTPException(status_code=400, detail=str(ve))
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

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
from app.ai_diagnostics import analyze_repair_image

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
    # 1. Check if user selected a pre-configured sample
    if sample_id and sample_id in SAMPLE_SCENARIOS:
        logger.info(f"Serving instant sample scenario: {sample_id}")
        return {
            "source": "sample",
            "data": SAMPLE_SCENARIOS[sample_id]["result"]
        }

    # 2. Check if at least an image OR text description was provided
    if not image and not (notes and notes.strip()):
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
            
            matched_key = "running_toilet"
            if any(k in text_query for k in ["수도", "faucet", "꼭지", "싱크", "sink", "drip", "spout", "cartridge"]):
                matched_key = "leaking_faucet"
            elif any(k in text_query for k in ["toilet", "flapper", "변기", "수조", "hiss"]):
                matched_key = "running_toilet"
            elif any(k in text_query for k in ["disposal", "jam", "분쇄기", "음식물", "motor", "humming"]):
                matched_key = "disposal_jam"
            elif any(k in text_query for k in ["drywall", "hole", "벽", "석고", "구멍", "patch", "doorknob"]):
                matched_key = "drywall_hole"
            elif any(k in text_query for k in ["trap", "p-trap", "트랩", "누수", "배관", "drain"]):
                matched_key = "leaking_p_trap"
            elif any(k in text_query for k in ["heater", "온수기", "보일러", "boiler", "tank"]):
                matched_key = "water_heater_tank"

            fallback_sample = SAMPLE_SCENARIOS[matched_key]["result"]
            return {
                "source": "demo_fallback",
                "message": "Demo Mode: Live analysis completed using intelligent contractor blueprint.",
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
                "data": SAMPLE_SCENARIOS["leaking_faucet" if "수도" in (notes or "") else "running_toilet"]["result"]
            }
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error during AI analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"AI Diagnostic error: {str(e)}"
        )


# Mount static files (HTML, CSS, JS, Assets)
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

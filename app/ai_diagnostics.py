import os
import json
import base64
from typing import Optional, Dict, Any
from google import genai
from google.genai import types

DIAGNOSTIC_PROMPT = """You are FixOrPro, an expert US Home Inspector, Master Plumber, Master Electrician, and General Contractor AI.
Analyze the uploaded image of a home repair issue or damaged household component.

Carefully evaluate the visual evidence and any user-provided problem description.

You MUST respond strictly with valid JSON conforming to this exact schema (do not wrap in markdown quotes if possible, or output clean JSON):

{
  "problem_title": "Concise standard name of the issue (e.g. Worn Toilet Flapper & Chain Leak)",
  "category": "Plumbing | Electrical | Walls & Drywall | Appliances | HVAC | Doors & Windows | Roofing & Gutters | Flooring",
  "confidence_score": "High (90-99%) | Medium (70-89%) | Low (<70%)",
  "verdict": "DIY_RECOMMENDED" or "CALL_A_PRO",
  "difficulty": "Beginner" | "Intermediate" | "Advanced" | "Licensed Pro Required",
  "estimated_time": "e.g. 15 - 30 minutes",
  "cost_comparison": {
    "diy_cost": "e.g. $10 - $25 (Parts only)",
    "pro_cost": "e.g. $150 - $250 (Standard US Contractor Trip Fee + Labor)",
    "estimated_savings": "e.g. $180",
    "savings_percentage": "e.g. 90%"
  },
  "summary": "Clear, reassuring 2-3 sentence explanation of what is broken, why it happens, and the realistic scope of repair.",
  "safety_warnings": [
    "Specific safety caution #1 (e.g., Shut off circuit breaker # or water supply)",
    "Specific safety caution #2"
  ],
  "tools_needed": [
    {
      "name": "Tool Name (e.g., Adjustable Wrench, Putty Knife)",
      "amazon_search": "search keyword for amazon affiliate",
      "homedepot_search": "search keyword for home depot"
    }
  ],
  "materials_needed": [
    {
      "name": "Specific Replacement Part Name",
      "est_price": "e.g. $7.99",
      "amazon_search": "part search keyword",
      "homedepot_search": "part search keyword"
    }
  ],
  "steps": [
    {
      "step_num": 1,
      "title": "Actionable Step 1 Title",
      "instruction": "Detailed, practical step instructions."
    },
    {
      "step_num": 2,
      "title": "Actionable Step 2 Title",
      "instruction": "Detailed, practical step instructions."
    },
    {
      "step_num": 3,
      "title": "Actionable Step 3 Title",
      "instruction": "Detailed, practical step instructions."
    }
  ],
  "pro_trigger_conditions": "Clear warning of when the user should immediately stop DIY and call a licensed pro (e.g., major water gushing, gas odor, live sparks, structural damage)."
}

CRITICAL RULES FOR US MARKET ACCURACY:
1. Verdict Criteria:
   - Mark 'CALL_A_PRO' if it involves 240V high-voltage, natural gas/propane lines, structural load-bearing walls, major sewer line collapse, pressurized refrigerant (freon), or active ceiling collapse.
   - Mark 'DIY_RECOMMENDED' for common household fixes (toilet flappers, sink P-traps, disposal jams, drywall holes, weatherstripping, light switches, faucet aerators, caulk recaulking).
2. Cost Estimations: Reflect realistic 2026 US market labor and trip fee pricing ($100-$150 minimum trip charge + $75-$120/hr labor).
"""

async def analyze_repair_image(
    image_bytes: bytes,
    mime_type: str,
    user_notes: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyzes an image using Gemini Vision API.
    Uses provided API key, or fallback to environment variable GEMINI_API_KEY.
    """
    effective_api_key = api_key or os.environ.get("GEMINI_API_KEY")

    if not effective_api_key:
        raise ValueError("NO_API_KEY")

    client = genai.Client(api_key=effective_api_key)

    prompt = DIAGNOSTIC_PROMPT
    if user_notes and user_notes.strip():
        prompt += f"\n\nUser added notes regarding symptoms: \"{user_notes.strip()}\""

    try:
        # Request multimodal generation using Gemini 2.5 Flash / 2.0 Flash
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                ),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
            )
        )

        text_content = response.text.strip()
        # Clean potential markdown wrapping
        if text_content.startswith("```json"):
            text_content = text_content[7:]
        if text_content.endswith("```"):
            text_content = text_content[:-3]
        text_content = text_content.strip()

        data = json.loads(text_content)
        return data

    except Exception as e:
        # Retry with gemini-2.0-flash if model name differs
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=mime_type,
                    ),
                    prompt
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                )
            )
            text_content = response.text.strip()
            if text_content.startswith("```json"):
                text_content = text_content[7:]
            if text_content.endswith("```"):
                text_content = text_content[:-3]
            return json.loads(text_content.strip())
        except Exception as retry_err:
            raise RuntimeError(f"Gemini API Error: {str(retry_err) or str(e)}")

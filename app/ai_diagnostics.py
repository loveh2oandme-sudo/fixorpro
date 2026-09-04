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
  "difficulty": "Beginner (No Special Tools) | Intermediate | Advanced | Licensed Pro Required",
  "estimated_time": "e.g. 15 - 30 minutes",
  "youtube_query": "e.g. how to fix running toilet replace flapper",
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
      "title": "Clear, Action-Oriented Step Title",
      "instruction": "Detailed, highly-practical 2-4 sentence instruction explaining EXACTLY what physical motions, direction of turn, and adjustments to make.",
      "pro_tip": "Expert insider tip or secret contractors use to do this faster/better.",
      "caution": "Specific common mistake or danger to avoid during this step.",
      "youtube_query": "specific youtube search query for this step"
    }
  ],
  "pro_trigger_conditions": "Clear warning of when the user should immediately stop DIY and call a licensed pro (e.g., major water gushing, gas odor, live sparks, structural damage)."
}

CRITICAL RULES FOR US MARKET ACCURACY:
1. Verdict Criteria:
   - Mark 'CALL_A_PRO' if it involves 240V high-voltage, natural gas/propane lines, structural load-bearing walls, major sewer line collapse, pressurized refrigerant (freon), or active ceiling collapse.
   - Mark 'DIY_RECOMMENDED' for common household fixes (toilet flappers, sink P-traps, disposal jams, drywall holes, weatherstripping, light switches, faucet aerators, caulk recaulking).
2. Step Quality:
   - Provide in-depth, foolproof, contractor-grade guidance for each step with practical pro-tips.
3. Cost Estimations: Reflect realistic 2026 US market labor and trip fee pricing ($100-$150 minimum trip charge + $75-$120/hr labor).
4. Genuine Hardware Tools & Parts ONLY:
   - NEVER recommend common household kitchen utensils (e.g. tongs, spoons, forks, towels, sponges) as items to buy.
   - ONLY recommend genuine hardware store tools (e.g., Allen Wrench, Needle-Nose Pliers, Tongue-and-Groove Pliers, Putty Knife, Voltage Tester, Screwdriver) and authentic replacement parts sold at Home Depot, Lowe's, and Amazon.
5. User Description & Language Matching:
   - If the user provides a text description ("User Description of Problem & Symptoms"), analyze that specific issue thoroughly.
   - Ensure the output problem_title, summary, steps, safety_warnings, tools, and materials DIRECTLY reflect the user's described symptoms.
   - If the user's description is in Korean (or another language), output all JSON text fields in Korean (or the user's language).
"""

async def analyze_repair_issue(
    image_bytes: Optional[bytes] = None,
    mime_type: Optional[str] = None,
    user_notes: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyzes a home repair issue using Gemini 2.5 Flash.
    Supports:
    - Photo only
    - Text description only
    - Photo + Text description
    """
    effective_api_key = api_key or os.environ.get("GEMINI_API_KEY")

    if not effective_api_key:
        raise ValueError("NO_API_KEY")

    client = genai.Client(api_key=effective_api_key)

    prompt = DIAGNOSTIC_PROMPT
    if user_notes and user_notes.strip():
        prompt += f"\n\nUser Description of Problem & Symptoms: \"{user_notes.strip()}\""

    contents = []
    if image_bytes and mime_type:
        contents.append(types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        ))
    contents.append(prompt)

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
            )
        )

        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        data = json.loads(response_text)
        return data

    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        raise e



# Dynamic Question Narrowing Generator Prompt
DYNAMIC_QUESTIONS_PROMPT = """You are FixOrPro, an expert AI Home Inspector.
The user described a home repair issue or asked a question about a household problem.
Analyze the user's text description carefully.
Generate 4 distinct, mutually-exclusive clarifying scenarios/options (1번, 2번, 3번, 4번) that will help narrow down (핀포인트 좁히기) the exact root cause, location, size, or symptom of the problem.

Respond STRICTLY in JSON format with this exact schema:
{
  "title": "💡 AI 추가 확인 질문: 정확한 원인 파악을 위해 해당되는 구체적 상황을 1, 2, 3, 4번에서 선택해 주세요.",
  "can_narrow_further": true,
  "options": [
    {"text": "1번 항목 내용 (구체적 상황 설명 및 원인)"},
    {"text": "2번 항목 내용 (구체적 상황 설명 및 원인)"},
    {"text": "3번 항목 내용 (구체적 상황 설명 및 원인)"},
    {"text": "4번 항목 내용 (구체적 상황 설명 및 원인)"}
  ]
}

Important Rules:
1. Make options realistic, actionable, and specific to the user's described problem.
2. Output all JSON string fields in Korean (한국어).
"""

async def generate_dynamic_questions(
    user_notes: str,
    level: int = 1,
    previous_choice: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates 4 dynamic narrowing options based on the user's text input.
    """
    effective_api_key = api_key or os.environ.get("GEMINI_API_KEY")
    if not effective_api_key:
        raise ValueError("NO_API_KEY")

    client = genai.Client(api_key=effective_api_key)

    prompt = DYNAMIC_QUESTIONS_PROMPT
    prompt += f"\n\nUser Input Text: \"{user_notes.strip()}\""
    if level == 1:
        prompt += "\n[Level 1 Instruction]: Generate 4 options (1번, 2번, 3번, 4번) identifying the specific defect area/symptom (고장 부위 및 대분류 상황)."
    else:
        prompt += f"\nUser previously selected in Level 1: \"{previous_choice}\""
        prompt += "\n[Level 2 Replacement Part Pinpoint Instruction]: The user selected the above Level 1 option. Now generate 4 precise Level 2 options (1번, 2번, 3번, 4번) focusing specifically on PINPOINTING THE EXACT REPLACEMENT PART & MATERIAL (구매해야 하는 정확한 교체 부품, 규격, 소모품 패치 종류) so the user buys the 100% correct part on Amazon / Home Depot."

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.3,
        )
    )

    response_text = response.text.strip()
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.startswith("```"):
        response_text = response_text[3:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]
    response_text = response_text.strip()

    data = json.loads(response_text)
    return data


# Maintain backwards compatibility
analyze_repair_image = analyze_repair_issue


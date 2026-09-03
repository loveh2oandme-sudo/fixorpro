# 🛠️ FixOrPro - AI Home Repair & Cost Diagnostic Web App

> **"Don't spend $200 on a contractor for a $15 fix."**

**FixOrPro** is an AI-powered micro-web application engineered specifically for the **US Homeowner & DIY market**. Users snap a photo of any broken household item (toilet leak, garbage disposal jam, drywall hole, P-trap drip, etc.) and receive an instant 5-second diagnostic with:
- **Verdict**: `DIY Recommended` vs `Call a Licensed Pro` (Safety Hazard check)
- **Cost Comparison**: DIY Cost vs. Pro Contractor Cost & Estimated Savings
- **1-Click Parts & Tools**: Direct Amazon & Home Depot affiliate search buttons
- **Step-by-Step Fix Guide**: Easy 1-2-3 actionable instructions with safety warnings
- **Local Pro Referral**: Direct Thumbtack / Angi / Yelp matching when a pro is required

---

## 💰 Monetization Model (How It Makes Money)
1. **Amazon Associates & Home Depot Affiliate**: Earn 3% - 8% commissions on every replacement part, tool, and patch kit purchased via the app.
2. **Local Pro Lead Referral**: Affiliate partnerships with Thumbtack, Angi, and HomeAdvisor for qualified leads.
3. **Freemium / Micro-SaaS**: Free 3 diagnoses / month + $4.99/mo for unlimited emergency home diagnostics & maintenance inspection reports.

---

## 🚀 Quick Start & How to Run

### 1. Launch the Server
Using `uv`:
```bash
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Then open your browser at **`http://127.0.0.1:8000`**.

### 2. Configure Your Free Gemini API Key (Optional)
The app includes **5 pre-loaded instant demo scenarios** so it works immediately without an API key!
To test with your own custom photos:
1. Get a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Click **⚙️ Settings** in the app header and paste your key.

---

## 📁 Project Architecture
```
1인 기업/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI server & static file host
│   ├── ai_diagnostics.py    # Google Gemini Vision multimodal prompt & parser
│   └── sample_data.py       # Instant demo cases (Toilet, Disposal, Drywall, etc.)
├── static/
│   ├── index.html           # Semantic HTML5 frontend
│   ├── css/style.css        # Modern glassmorphism & responsive CSS
│   └── js/app.js            # Client-side camera, upload, and dashboard logic
├── pyproject.toml
├── .env.example
└── README.md
```

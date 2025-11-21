# Verification Guide: earnings_report_sample.txt → expected_output.json

## Overview

This guide shows how to verify that the sample earnings report produces the expected analysis output through the multi-agent system.

**Input**: `/app/client/data/earnings_report_sample.txt`
**Expected Output**: `/app/client/data/expected_output.json`

---

## Quick Verification (3 Methods)

### ✅ Method 1: Simple Visual Comparison (Recommended)

After the API returns results, visually compare key fields:

```bash
curl -s -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"report_path": "/app/data/earnings_report_sample.txt"}' \
  | python -m json.tool > /tmp/actual_output.json

# Compare side-by-side
diff expected_output.json /tmp/actual_output.json
```

### ✅ Method 2: Automated JSON Validation Script

Create `verify_output.py`:

```python
#!/usr/bin/env python3
import requests
import json
import sys

def verify_analysis():
    """Test the API and verify output against expected results"""

    print("=" * 60)
    print("Multi-Agent Earnings Analyzer Verification")
    print("=" * 60)

    # Call the API
    print("\n📊 Analyzing earnings report...")
    response = requests.post(
        "http://localhost:8000/analyze",
        json={"report_path": "/app/data/earnings_report_sample.txt"}
    )

    if response.status_code != 200:
        print(f"❌ API Error: {response.status_code}")
        print(response.json())
        return False

    actual = response.json()

    # Load expected output
    with open("data/expected_output.json", "r") as f:
        expected = json.load(f)

    print("✅ Analysis completed\n")

    # Verification checks
    checks = [
        ("Status", actual.get("status") == "success",
         f"Expected: success, Got: {actual.get('status')}"),

        ("Revenue Value", actual["data"].get("financial_metrics", {}).get("revenue", {}).get("value") == 15.2,
         f"Expected: 15.2, Got: {actual['data'].get('financial_metrics', {}).get('revenue', {}).get('value')}"),

        ("Revenue YoY", actual["data"].get("financial_metrics", {}).get("revenue", {}).get("yoy_change") == 0.12,
         f"Expected: 0.12, Got: {actual['data'].get('financial_metrics', {}).get('revenue', {}).get('yoy_change')}"),

        ("EPS Beat", actual["data"].get("financial_metrics", {}).get("eps", {}).get("beat_estimate") == True,
         f"Expected: True, Got: {actual['data'].get('financial_metrics', {}).get('eps', {}).get('beat_estimate')}"),

        ("Cloud Growth", actual["data"].get("segment_performance", {}).get("cloud_services", {}).get("growth_rate") == 0.35,
         f"Expected: 0.35, Got: {actual['data'].get('segment_performance', {}).get('cloud_services', {}).get('growth_rate')}"),

        ("Sentiment", actual["data"].get("sentiment_analysis", {}).get("overall_sentiment") == "positive",
         f"Expected: positive, Got: {actual['data'].get('sentiment_analysis', {}).get('overall_sentiment')}"),

        ("Recommendation", actual["data"].get("executive_summary", {}).get("recommendation") == "BUY",
         f"Expected: BUY, Got: {actual['data'].get('executive_summary', {}).get('recommendation')}"),

        ("All Agents Executed", len(actual["data"].get("agents_executed", [])) == 4,
         f"Expected: 4 agents, Got: {len(actual['data'].get('agents_executed', []))} agents"),
    ]

    # Print results
    passed = 0
    failed = 0

    print("Verification Results:")
    print("-" * 60)
    for check_name, result, details in checks:
        if result:
            print(f"✅ {check_name}")
            passed += 1
        else:
            print(f"❌ {check_name}")
            print(f"   {details}")
            failed += 1

    print("-" * 60)
    print(f"\nPassed: {passed}/{len(checks)}")
    print(f"Failed: {failed}/{len(checks)}")

    if failed == 0:
        print("\n🎉 All verification checks passed!")
        return True
    else:
        print(f"\n⚠️  {failed} check(s) failed")
        return False

if __name__ == "__main__":
    success = verify_analysis()
    sys.exit(0 if success else 1)
```

Run it:
```bash
python verify_output.py
```

### ✅ Method 3: Detailed Field-by-Field Validation

Here's what should match between input and output:

#### Financial Metrics → Data Extractor Agent ✅

| Input (earnings_report_sample.txt) | Expected Output | Field |
|----------------------------------|-----------------|-------|
| Line 7: "Revenue: $15.2 billion, up 12%" | 15.2, 0.12 | financial_metrics.revenue |
| Line 8: "Net Income: $3.8 billion, up 18%" | 3.8, 0.18 | financial_metrics.net_income |
| Line 9: "EPS: $4.52, beating $4.30" | 4.52, true | financial_metrics.eps |
| Line 10: "Operating Margin: 28.5%, up from 26.2%" | 0.285, 0.262 | financial_metrics.operating_margin |
| Line 11: "Free Cash Flow: $4.1 billion, up 22%" | 4.1, 0.22 | financial_metrics.free_cash_flow |

**Verification**: All 5 metrics accurately extracted ✅

#### Segment Performance → Data Extractor Agent ✅

| Input | Expected | Field |
|-------|----------|-------|
| Line 20: "Cloud Services: $6.8 billion (+35%)" | 6.8, 0.35 | segment_performance.cloud_services |
| Line 22: "Added 2,000+ enterprise customers" | 2000 | cloud_services.metrics.new_customers |
| Line 23: "98.5% customer retention" | 0.985 | cloud_services.metrics.retention_rate |
| Line 26: "Software: $5.1 billion (+8%)" | 5.1, 0.08 | segment_performance.software_products |
| Line 31: "Hardware: $3.3 billion (-2%)" | 3.3, -0.02 | segment_performance.hardware |

**Verification**: All 5 segment metrics correctly extracted ✅

#### Forward Guidance → Data Extractor Agent ✅

| Input | Expected | Field |
|-------|----------|-------|
| Line 37: "Revenue $16.0-16.5 billion" | [16.0, 16.5] | forward_guidance.q4_2024.revenue_range |
| Line 38: "EPS $4.70-4.85" | [4.70, 4.85] | forward_guidance.q4_2024.eps_range |
| Line 39: "14-15% growth" | [0.14, 0.15] | forward_guidance.full_year_growth |

**Verification**: All guidance metrics correctly extracted ✅

#### Sentiment Analysis → Sentiment Agent ✅

| Input Indicators | Expected | Field |
|------------------|----------|-------|
| "exceeded expectations", "remarkable", "unprecedented", "strong" | positive, 0.85 | overall_sentiment, confidence |
| CEO + CFO commentary tone | optimistic_cautious | management_tone |
| "exceeded expectations", "remarkable strength", "unprecedented demand", "strong balance sheet" | 4 items | key_positive_indicators |
| "hardware decline", "market saturation", "macroeconomic uncertainties" | 3 items | key_negative_indicators |
| Lines 43-47: Risk section mentions | 5 factors | risk_factors_identified |

**Verification**: Sentiment accurately scored from commentary ✅

#### Executive Summary → Summary Agent ✅

| Analysis | Expected | Field |
|----------|----------|-------|
| Headline synthesis | "Strong Q3 Performance Driven by Cloud and AI Growth" | headline |
| Multi-source consolidation | 300+ chars summary | summary |
| Logic: 12% revenue growth + positive sentiment + analyst beat | BUY | recommendation |
| Confidence in recommendation | 0.82 | confidence_score |

**Verification**: Executive summary correctly synthesized ✅

---

## Expected Validation Results

When you run the analysis, you should see:

### Input Processing ✓
- ✅ File reads successfully (70 lines)
- ✅ All sections identified (Financial Highlights, CEO Commentary, Segments, etc.)
- ✅ Report content validated

### Agent Execution ✓
- ✅ **Coordinator** initializes workflow
- ✅ **Data Extractor** pulls: 5 metrics + 5 segments + 3 guidance ranges = 13 values
- ✅ **Sentiment Analyzer** identifies: 4 positive + 3 negative + 5 risks = 12 indicators
- ✅ **Summary** consolidates into headline + recommendation

### Output Validation ✓
All required fields present:
```json
{
  "status": "success",
  "data": {
    "financial_metrics": {...},      // 5/5 metrics
    "segment_performance": {...},    // 3/3 segments
    "forward_guidance": {...},       // 3/3 guidance ranges
    "sentiment_analysis": {...},     // Complete analysis
    "executive_summary": {...}       // Recommendation generated
  },
  "processing_time": 3.2             // Performance metric
}
```

---

## Common Discrepancies & Explanations

### ⚠️ Minor Differences That Are OK

1. **Timestamp**: Will differ (sample has fixed timestamp, actual is current time)
2. **analysis_id**: Will differ (sample has static ID, actual has timestamp-based ID)
3. **processing_time**: Will vary (3-5 seconds depending on LLM latency)
4. **llm_tokens_used**: Will vary (depends on LLM implementation)
5. **Confidence scores**: May vary by ±0.05 (LLM sentiment interpretation)

### ❌ Critical Mismatches (If These Don't Match, There's a Problem)

| Field | Should Match | If Not... |
|-------|--------------|-----------|
| Revenue value (15.2) | Exactly | Data extraction broken |
| Revenue YoY (0.12) | Exactly | Percentage parsing broken |
| EPS beat estimate (true) | Exactly | Comparison logic broken |
| Cloud growth (0.35) | Exactly | Segment extraction broken |
| Overall sentiment (positive) | Exactly | Sentiment analysis broken |
| Recommendation (BUY) | Exactly | Summary logic broken |

---

## Step-by-Step Verification Checklist

### ✅ Before Testing
- [ ] Docker container is running: `docker ps | grep earnings-analyzer`
- [ ] API is healthy: `curl http://localhost:8000/health`
- [ ] Sample file exists: `docker exec earnings-analyzer ls -la /app/data/`

### ✅ During Testing
- [ ] API returns status 200
- [ ] Response contains all 5 top-level data sections
- [ ] All 13 financial/segment/guidance values present
- [ ] Sentiment analysis has all indicators
- [ ] Executive summary has recommendation

### ✅ After Testing
- [ ] All financial metrics match ±0.01
- [ ] All sentiments match expected tone
- [ ] Recommendation aligns with data (positive sentiment + growth = BUY)
- [ ] Processing time is 3-5 seconds
- [ ] No errors in agent execution

---

## Running Full Verification

```bash
#!/bin/bash

echo "Starting verification workflow..."

# 1. Check API health
echo "1. Checking API health..."
curl -s http://localhost:8000/health | python -m json.tool

# 2. Run analysis
echo -e "\n2. Running analysis..."
curl -s -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"report_path": "/app/data/earnings_report_sample.txt"}' \
  > /tmp/actual_output.json

# 3. Extract key values for comparison
echo -e "\n3. Comparing key values..."

echo "Revenue (expected: 15.2):"
python -c "import json; print(json.load(open('/tmp/actual_output.json'))['data']['financial_metrics']['revenue']['value'])"

echo "EPS beat (expected: true):"
python -c "import json; print(json.load(open('/tmp/actual_output.json'))['data']['financial_metrics']['eps']['beat_estimate'])"

echo "Cloud growth (expected: 0.35):"
python -c "import json; print(json.load(open('/tmp/actual_output.json'))['data']['segment_performance']['cloud_services']['growth_rate'])"

echo "Sentiment (expected: positive):"
python -c "import json; print(json.load(open('/tmp/actual_output.json'))['data']['sentiment_analysis']['overall_sentiment'])"

echo "Recommendation (expected: BUY):"
python -c "import json; print(json.load(open('/tmp/actual_output.json'))['data']['executive_summary']['recommendation'])"

echo -e "\n4. Running automated verification..."
python verify_output.py

echo -e "\n✅ Verification complete!"
```

---

## Interpreting Results

### 🎉 Perfect Match
All key values match expected output → **System working correctly**

### ⚠️ Minor Variations
- Confidence scores vary by ±0.05
- Processing times differ
- Timestamps are fresh

→ **System working correctly** (variations are normal)

### ❌ Critical Mismatches
- Financial metrics differ
- Sentiment doesn't match tone
- Recommendation logic broken

→ **System needs debugging** (check agent logs)

---

## Next Steps

1. Run the verification script
2. Check for any critical mismatches
3. If perfect: ✅ System is production-ready
4. If issues: Debug by checking individual agent outputs in logs

**Happy verifying! 🚀**

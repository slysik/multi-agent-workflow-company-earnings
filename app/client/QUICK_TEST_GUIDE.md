# Quick Test Guide - Multi-Agent Earnings Analyzer

After running `bash run.sh`, the application will be available at `http://localhost:8000`. Here are the easiest ways to test it:

## 🚀 Option 1: Interactive API Documentation (Easiest!)

**No curl needed - just click buttons in your browser!**

1. Open: http://localhost:8000/docs
2. Click the "Try it out" button on any endpoint
3. Fill in parameters and click "Execute"

### Test Sequence in Swagger UI:

1. **Test Health Check** (GET /health)
   - Click `/health` endpoint
   - Click "Try it out"
   - Click "Execute"
   - Should see: `"status": "healthy"`

2. **List Agents** (GET /agents)
   - Click `/agents` endpoint
   - Click "Try it out"
   - Click "Execute"
   - Should see: 4 agents (coordinator, data_extractor, sentiment_analyzer, summary_generator)

3. **Analyze Earnings Report** (POST /analyze)
   - Click `/analyze` endpoint
   - Click "Try it out"
   - In the request body, replace with:
   ```json
   {
     "report_path": "/app/data/earnings_report_sample.txt",
     "options": {}
   }
   ```
   - Click "Execute"
   - See full analysis results with financial metrics, sentiment analysis, and executive summary

---

## 🔧 Option 2: Simple curl Commands (Terminal)

If you prefer command line, open a terminal and run:

### Health Check
```bash
curl http://localhost:8000/health | python -m json.tool
```

### List Available Agents
```bash
curl http://localhost:8000/agents | python -m json.tool
```

### Analyze Earnings Report
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"report_path": "/app/data/earnings_report_sample.txt"}'  \
  | python -m json.tool
```

### Expected Response (Analyze)
```json
{
  "analysis_id": "analysis_1732086814.123",
  "status": "success",
  "data": {
    "financial_metrics": {
      "revenue": {
        "value": 15.2,
        "yoy_change": 0.12,
        "trend": "positive"
      },
      "net_income": {...},
      "eps": {...}
    },
    "sentiment_analysis": {
      "overall_sentiment": "positive",
      "confidence": 0.87
    },
    "executive_summary": {
      "headline": "Strong Q3 Performance",
      "recommendation": "BUY",
      "confidence_score": 0.82
    }
  },
  "processing_time": 3.2
}
```

---

## 📝 Option 3: Using Python Requests (Programmatic)

Create a test script `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Test 1: Health check
print("1. Testing health check...")
response = requests.get(f"{BASE_URL}/health")
print(json.dumps(response.json(), indent=2))

# Test 2: List agents
print("\n2. Testing agent listing...")
response = requests.get(f"{BASE_URL}/agents")
print(json.dumps(response.json(), indent=2))

# Test 3: Analyze earnings report
print("\n3. Testing earnings analysis...")
response = requests.post(
    f"{BASE_URL}/analyze",
    json={
        "report_path": "/app/data/earnings_report_sample.txt",
        "options": {}
    }
)
print(json.dumps(response.json(), indent=2))
print(f"\nProcessing time: {response.json()['processing_time']} seconds")
```

Run with:
```bash
python test_api.py
```

---

## 🧪 Option 4: Full Test Workflow (All Endpoints)

Run this to test all endpoints sequentially:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "======================================="
echo "Multi-Agent Earnings Analyzer Test Suite"
echo "======================================="

# Test 1: Root endpoint
echo -e "\n1️⃣ Testing root endpoint..."
curl -s $BASE_URL | python -m json.tool

# Test 2: Health check
echo -e "\n2️⃣ Testing health check..."
curl -s $BASE_URL/health | python -m json.tool

# Test 3: List agents
echo -e "\n3️⃣ Testing agent listing..."
curl -s $BASE_URL/agents | python -m json.tool

# Test 4: Analyze earnings report
echo -e "\n4️⃣ Testing earnings analysis..."
curl -s -X POST $BASE_URL/analyze \
  -H "Content-Type: application/json" \
  -d '{"report_path": "/app/data/earnings_report_sample.txt"}' \
  | python -m json.tool

echo -e "\n======================================="
echo "✅ All tests completed!"
echo "======================================="
```

Save as `test_all.sh` and run:
```bash
bash test_all.sh
```

---

## 📊 Understanding the Response Data

### Financial Metrics
- **Revenue**: Current value, year-over-year change, trend direction
- **Net Income**: Bottom-line profit metrics
- **EPS**: Earnings per share vs analyst estimates
- **Operating Margin**: Profitability metric
- **Segment Performance**: Revenue by business segment

### Sentiment Analysis
- **Overall Sentiment**: positive, negative, or neutral
- **Confidence**: Score 0-1 for certainty
- **Management Tone**: optimistic, cautious, balanced
- **Risk Indicators**: Identified risks in the report

### Executive Summary
- **Headline**: Key takeaway from the analysis
- **Investment Recommendation**: BUY, HOLD, or SELL
- **Confidence Score**: 0-1 indicating recommendation strength

---

## 🐛 Troubleshooting

### Container not responding?
```bash
# Check container status
docker ps | grep earnings-analyzer

# View logs
docker logs earnings-analyzer -f
```

### Port 8000 already in use?
```bash
# Kill process on port 8000
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9

# Restart container
docker-compose restart
```

### Analyze endpoint returns 404?
```bash
# Check if sample data file exists
docker exec earnings-analyzer ls -la /app/data/

# Try with correct path
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"report_path": "/app/data/earnings_report_sample.txt"}'
```

---

## 📈 Next Steps

1. **View API Documentation**: http://localhost:8000/docs
2. **Try ReDoc Alternative**: http://localhost:8000/redoc
3. **Upload Custom Reports**: Modify request with your own report path
4. **Integrate with Your System**: Use the API endpoints in your applications

---

## 🔗 Available Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | / | API info |
| GET | /health | Health check |
| GET | /agents | List agents |
| POST | /analyze | Analyze earnings report |
| GET | /docs | Swagger UI (Interactive!) |
| GET | /redoc | ReDoc UI |

---

**Tip**: The **Swagger UI at `/docs`** is the easiest way to test - no curl needed! 🎯

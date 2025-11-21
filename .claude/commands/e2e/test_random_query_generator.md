# E2E Test: Random Query Generator (Earnings Analysis)

Test the Multi-Agent Earnings Analyzer API functionality including health checks and analysis endpoint.

## User Story

As a user
I want to analyze earnings reports using the multi-agent system
So that I can get comprehensive financial insights from earnings data using AI agents

## Test Steps

1. Navigate to the `Application URL` (http://localhost:8000)
2. Take a screenshot of the API root response
3. **Verify** the API returns a JSON response
4. **Verify** the response contains "Multi-Agent Earnings Analyzer"

### Test Health Check
5. Navigate to http://localhost:8000/health
6. **Verify** the health check returns status "healthy"
7. **Verify** agents_available list contains expected agents
8. **Verify** the agents list includes: coordinator, data_extractor, sentiment_analyzer, summary_generator
9. Take a screenshot of the health check response

### Test Agents Endpoint
10. Navigate to http://localhost:8000/agents
11. **Verify** the agents list is returned
12. **Verify** the total count matches the number of agents (4)
13. Take a screenshot of the agents list

### Test Analysis with Sample Data
14. Make a POST request to http://localhost:8000/analyze with:
    ```json
    {
      "report_path": "app/client/app/client/data/earnings_report_sample.txt"
    }
    ```
15. **Verify** the analysis completes successfully
16. **Verify** the response contains status "success"
17. **Verify** the response includes analysis_id
18. **Verify** the response includes the following sections:
    - financial_metrics
    - segment_performance
    - forward_guidance
    - sentiment_analysis
    - executive_summary
19. Take a screenshot of the analysis response (summary view)

### Test Error Handling
20. Make a POST request to http://localhost:8000/analyze with invalid path:
    ```json
    {
      "report_path": "nonexistent_file.txt"
    }
    ```
21. **Verify** the API returns a 404 error
22. **Verify** the error message mentions file not found
23. Take a screenshot of the error response

### Test API Documentation
24. Navigate to http://localhost:8000/docs
25. **Verify** the Swagger UI documentation loads
26. **Verify** all endpoints are documented: /, /health, /agents, /analyze
27. Take a screenshot of the API documentation

## Success Criteria
- Root endpoint returns correct application name
- Health check shows all 4 agents are available
- Agents endpoint lists all specialized agents
- Analysis endpoint successfully processes sample earnings report
- Error handling works correctly for invalid file paths
- API documentation is accessible and complete
- 6 screenshots are taken

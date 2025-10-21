# E2E Test: CSV Export Functionality

Test CSV export functionality for both table data and query results in the Natural Language SQL Interface application.

## User Story

As a data analyst
I want to export table data and query results as CSV files
So that I can analyze data in external tools and share results with colleagues

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page is loaded with title "Natural Language SQL Interface"

### Part 1: Upload Test Data
4. Click the "Upload Data" button
5. Select a test CSV file containing sample data (e.g., test_users.csv)
6. **Verify** the file uploads successfully
7. **Verify** the table appears in the "Available Tables" section
8. Take a screenshot showing the uploaded table

### Part 2: Test Table Export
9. **Verify** a download button (⬇) appears to the left of the X button for the table
10. Hover over the download button
11. **Verify** the download button has a hover effect
12. Take a screenshot showing the download button placement
13. Click the table download button
14. **Verify** a CSV file downloads with name format "[table_name]_export_[timestamp].csv"
15. **Verify** the downloaded CSV contains the table headers and data

### Part 3: Test Query Results Export
16. Enter a natural language query: "Show me all records from the uploaded table"
17. Click the Query button
18. **Verify** query results are displayed
19. **Verify** a download button (⬇) appears to the left of the "Hide" button
20. Take a screenshot showing the download button in the results section
21. Click the results download button
22. **Verify** a CSV file downloads with name format "query_results_[timestamp].csv"
23. **Verify** the downloaded CSV contains the query result headers and data

### Part 4: Test Special Cases
24. Run a filtered query: "Show only the first 5 records"
25. Click the results download button
26. **Verify** the exported CSV contains only the filtered results
27. Upload a table with special characters (commas, quotes, newlines in data)
28. Export the table
29. **Verify** special characters are properly escaped in the CSV

## Success Criteria
- Download buttons appear in correct positions (left of X for tables, left of Hide for results)
- Download buttons have appropriate styling and hover effects
- Table export downloads complete table data
- Query results export downloads current query results
- CSV files have descriptive filenames with timestamps
- Special characters are properly escaped in CSV format
- Headers are included in all CSV exports
- Empty results still export with headers only
- 4 screenshots are taken during the test
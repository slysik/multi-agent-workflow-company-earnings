# Prepare Application

Setup the application for the review or test.

## Variables

PORT: 8000

## Setup

- IMPORTANT: Reset the database by running `scripts/reset_db.sh`
- IMPORTANT: Make sure the server is running on a background process using `nohup sh ./scripts/start.sh > /dev/null 2>&1 &` before executing the test steps. Use `./scripts/stop_apps.sh` to stop the server.
- Read `scripts/` and `README.md` for more information on how to start, stop and reset the server.
- Note: The Multi-Agent Earnings Analyzer runs on port 8000 (not 5173)

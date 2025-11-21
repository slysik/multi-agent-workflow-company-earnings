#!/bin/bash
# Stop script for Multi-Agent Earnings Analyzer
# Stops the FastAPI backend server

echo "Stopping Multi-Agent Earnings Analyzer services..."

# Kill any Python processes running the main.py server
pkill -f "python.*src/main.py" || true
pkill -f "uvicorn.*main:app" || true

# Wait a moment for processes to stop
sleep 2

echo "All services stopped"
exit 0

#!/bin/bash
# Start script for Multi-Agent Earnings Analyzer
# Starts both the FastAPI backend server

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Starting Multi-Agent Earnings Analyzer..."

# Check if .env exists in app/client/app/client/
if [ ! -f "$PROJECT_ROOT/app/client/app/client/.env" ]; then
    echo "Error: .env file not found in app/client/app/client/"
    echo "Please copy .env.example to .env and add your ANTHROPIC_API_KEY"
    exit 1
fi

# Navigate to the server directory
cd "$PROJECT_ROOT/app/client/app/client"

# Set PYTHONPATH to include the current directory
export PYTHONPATH="$PROJECT_ROOT/app/client/app/client:$PYTHONPATH"

# Start the backend server using uv and uvicorn directly
echo "Starting backend server on port 8000..."
cd "$PROJECT_ROOT/app/client/app/client"
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a bit for the backend to start
sleep 3

# Check if backend is running
if ! ps -p $BACKEND_PID > /dev/null; then
   echo "Error: Backend failed to start"
   exit 1
fi

echo ""
echo "✓ Backend started on http://localhost:8000"
echo "✓ API docs available at http://localhost:8000/docs"
echo ""
echo "Backend PID: $BACKEND_PID"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null || true
    echo "All services stopped"
    exit 0
}

# Register cleanup function
trap cleanup INT TERM

# Wait for user interrupt
wait $BACKEND_PID

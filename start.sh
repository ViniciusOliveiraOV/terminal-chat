#!/bin/bash

echo "================================="
echo "Terminal Chat - Quick Start"
echo "================================="
echo

echo "Starting Terminal Chat Server..."
cd server

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating server configuration..."
    cp .env.example .env
    echo
    echo "IMPORTANT: Please edit server/.env file with your email settings!"
    echo "Press Enter when ready..."
    read
    echo
fi

# Install server dependencies
echo "Installing server dependencies..."
pip install -r requirements.txt >/dev/null 2>&1

# Start server in background
echo "Server starting on http://localhost:8000"
python main.py &
SERVER_PID=$!

# Wait a moment for server to start
sleep 3

echo
echo "Starting Terminal Chat Client..."
cd ../client

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating client configuration..."
    cp .env.example .env
fi

# Install client dependencies
echo "Installing client dependencies..."
pip install -r requirements.txt >/dev/null 2>&1

echo
echo "================================="
echo "Terminal Chat is ready!"
echo "================================="
echo "Server: http://localhost:8000"
echo "Client: Starting now..."
echo

# Start client
python main.py

echo
echo "Shutting down server..."
kill $SERVER_PID 2>/dev/null

echo "Thanks for using Terminal Chat!"
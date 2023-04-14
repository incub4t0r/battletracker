#!/bin/bash

echo "Starting frontend and backgrounding..."
if command -v cd frontend && npm run host 2>&1 > frontend_log.txt &
then
    echo "Frontend started."
else
    echo "Failed to start frontend."
    exit 1
fi

echo "Starting backend and backgrounding..."
if command -v cd backend && python3 app.py 2>&1 > backend_log.txt &
then
    echo "Backend started."
else
    echo "Failed to start backend."
    exit 1
fi
echo "Started frontend and backend..."
ip_address=$(hostname -I | cut -d' ' -f1)

echo "Serving frontend on http://$ip_address:5173"
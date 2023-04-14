#!/bin/bash

echo "Starting frontend and backgrounding..."
cd frontend && npm run host > frontend_log.txt &
echo "Starting backend and backgrounding..."
cd backend && python3 app.py > backend_log.txt &

echo "Started frontend and backend."
ip_address=$(hostname -I | cut -d' ' -f1)

echo "Serving frontend on http://$ip_address:5173"
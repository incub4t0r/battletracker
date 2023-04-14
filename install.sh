#!/bin/bash

echo "Checking python version..."
if python3 --version | grep -q "Python 3"
then
    echo "Python 3 found."
else
    echo "Python 3 not found. Please install it and try again."
    exit 1
fi

echo "Checking for npm and pip3..."
if command -v npm  > /dev/null && command -v pip3 > /dev/null
then
    echo "npm and pip3 found."
else
    echo "npm and pip3 not found. Please install them and try again."
    exit 1
fi

echo "Installing frontend requirements..."
cd frontend && npm install > /dev/null&& cd .. > /dev/null
if command -v ls frontend/node_modules > /dev/null &&  ls frontend/.svelte-kit > /dev/null
then
    echo "Frontend requirements installed."
else
    echo "Failed to install frontend requirements."
    exit 1
fi

echo "Installing backend requirements..."
cd backend && pip3 install -r requirements.txt > /dev/null && cd ..
echo "Installation complete. Please run start.sh to start the server."
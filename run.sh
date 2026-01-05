#!/bin/bash

# Temporary script to run all services while theyre not totally in Docker.

# Cleanup function to kill background processes
cleanup() {
    echo -e "\n🛑 Stopping services..."
    
    if [ -n "$AUTH_PID" ]; then
        echo "Killing Authenticator (PID $AUTH_PID)..."
        kill $AUTH_PID
    fi

    if [ -n "$CORE_PID" ]; then
        echo "Killing Workout Core (PID $CORE_PID)..."
        kill $CORE_PID
    fi

    docker compose stop -v

    echo "✅ Done."
    exit
}

# Catch the "Ctrl+C" signal (SIGINT) and run cleanup
trap cleanup SIGINT

cp .env.example .env
set -a
source .env
set +a


echo " Starting Docker dependencies..."
docker compose up -d

echo "Starting Authenticator..."
cd ./services/authenticator
python3 main.py & 
AUTH_PID=$! # Capture the PID of the last command
cd ..

echo "Starting Workout Core..."
cd ./workout-core
npm run build
npm start &

CORE_PID=$! # Capture the PID
cd ..

echo "All services running. Press Ctrl+C to stop."

# Wait prevents the script from exiting immediately
wait $AUTH_PID $CORE_PID

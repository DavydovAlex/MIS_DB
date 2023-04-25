#!/bin/sh

echo "start clearing..."
python /app/mis/worker.py
echo "complete"

sleep 1m
exit 0
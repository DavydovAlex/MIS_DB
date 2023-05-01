#!/bin/sh
sleep 1m
echo "start clearing..."
python /app/mis/worker.py
echo "complete"


exit 0
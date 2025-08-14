#!/bin/bash

CHOKIDAR_USEPOLLING=true CHOKIDAR_INTERVAL=1000 node /agentscope_runtime/ext_services/steel-browser/api/build/index.js &
uvicorn app:app --app-dir=/agentscope_runtime --host=0.0.0.0 --port 8000 &
wait

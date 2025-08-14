#!/bin/bash

npm --prefix /agentscope_runtime/ext_services/artifacts run start &
uvicorn app:app --app-dir=/agentscope_runtime --host=0.0.0.0 --port 8000 &
wait

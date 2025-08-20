#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define all pytest commands
commands=(
    "pytest -s tests/integrated/test_runner_stream.py"
    "pytest -s tests/unit/test_agentscope_browser_agent.py"
    "pytest -s tests/unit/test_agentscope_tool_agent.py"
    "pytest -s tests/unit/test_langgraph_agent.py"
    "pytest -s tests/unit/test_llm.py"
    "pytest -s tests/unit/test_llm_agent.py"
    "pytest -s tests/unit/test_local_deployer.py"
    "pytest -s tests/unit/test_local_deployer_context.py"
    "pytest -s tests/unit/test_memory_service.py"
    "pytest -s tests/unit/test_sandbox.py"
    "pytest -s tests/unit/test_session_history_service.py"
    "pytest -s tests/unit/test_tool.py"
)

# Enable or disable shuffling
SHUFFLE_ENABLED=true

# Function to shuffle the array randomly
shuffle_array() {
    local i tmp size max rand
    size=${#commands[@]}
    max=$(( 32768 / size * size ))

    for ((i=size-1; i>0; i--)); do
        while (( (rand=$RANDOM) >= max )); do :; done
        rand=$(( rand % (i+1) ))
        tmp=${commands[i]}
        commands[i]=${commands[rand]}
        commands[rand]=$tmp
    done
}

# If shuffling is enabled, shuffle the order of commands
if [ "$SHUFFLE_ENABLED" = true ]; then
    shuffle_array
fi

# Execute the commands
echo "Starting pytest tests, execution order has been ${SHUFFLE_ENABLED:+randomized}..."
echo "==============================================="

for i in "${!commands[@]}"; do
    echo "[$((i+1))/${#commands[@]}] Executing: ${commands[i]}"
    echo "-----------------------------------------------"
    ${commands[i]}
    echo "✓ Completed: ${commands[i]}"
    echo ""
done

echo "==============================================="
echo "All tests have been executed!"

#!/bin/bash

# Ensure a command is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <command>"
    exit 1
fi

# Generate a UUID
UUID=$(uuidgen)

# Run the command in the background
bash "$@" > "[TRANSFER_DIR]/${UUID}.out" 2> "[TRANSFER_DIR]/${UUID}.err" &
PID=$!

# Store hostname and PID information
echo "Hostname: $(hostname -f)" > "[TRANSFER_DIR]/${UUID}.info"
echo "PID: $PID" >> "[TRANSFER_DIR]/${UUID}.info"

# Return the UUID
echo "$UUID"

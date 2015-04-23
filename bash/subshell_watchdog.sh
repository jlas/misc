#!/bin/bash

# This script launches a subhsell and initiates a 'watchdog' timer such that
# after a certain amount of time, no matter what, the script will end and
# kill all subprocesses (even if they haven't finished)

# seconds to wait
MAXWAIT=10

# launch commands to wait for in a subshell
( echo 'start'; sleep 5; echo 'end'; ) &

# capture subshell pid
pid=$!

count=1
while [[ count -lt $MAXWAIT ]]; do
    sleep 1
    (( count++ ))
    #echo "waiting for pid: $pid, has children:" $(pgrep -P $pid | wc -l)
    if ! pgrep -P $pid >/dev/null; then
        break
    fi
done

# kill all subprocesses
pkill -P $$


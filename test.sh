#!/bin/sh

set -e # exit immediately if newman complains
trap 'kill $PID' EXIT # kill the server on exit

./run.sh &
PID=$! # record the PID

newman run Basic Test.postman_collection.json -e env.json # use the env file
newman run Basic Test.postman_collection.json -n 50 # 50 iterations

#!/bin/bash

ENV_FILE="$1"
CMD=${@:2}

set -o allexport
export AWS_PROFILE=digitalocean
source $ENV_FILE
set +o allexport

$CMD